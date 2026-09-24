import { createClient } from 'https://cdn.jsdelivr.net/npm/@insforge/sdk@latest/+esm'

// InsForge Configuration
const insforgeUrl = 'https://6rdjtbz5.us-east.insforge.app';
const insforgeKey = 'ik_6c60f862a0fa7b76aa26ddd3210f7772';
const supabase = createClient({ baseUrl: insforgeUrl, anonKey: insforgeKey });

// Global State
window.currentUser = null;
window.intendedAuthAction = null;

// Expose requireAuthentication globally
window.requireAuthentication = function(featureName, callback) {
    if (window.currentUser) {
        if (callback) callback();
        return true;
    }
    
    // Unauthenticated: Show modal and save callback
    window.intendedAuthAction = callback;
    const overlay = document.getElementById('macro-auth-overlay');
    
    if (overlay) {
        const title = overlay.querySelector('h3');
        const desc = overlay.querySelector('p');
        if (title) title.innerText = `Sign in to unlock ${featureName}`;
        if (desc) desc.innerText = `Access advanced market-wide sentiment intelligence after signing in.`;
        
        overlay.classList.remove('hidden');
        overlay.classList.add('opacity-100');
        overlay.style.pointerEvents = 'auto';
    }
    return false;
};

// Intercept Protected Actions
document.addEventListener('click', (e) => {
    // Intercept navigation links
    const navLink = e.target.closest('a[href="#macro-analysis"], a[href="#view-macro"]');
    if (navLink) {
        if (!window.currentUser) {
            e.preventDefault();
            e.stopPropagation();
            window.requireAuthentication('Macro Analysis', () => {
                const targetId = navLink.getAttribute('href');
                document.querySelector(targetId)?.scrollIntoView({ behavior: 'smooth' });
            });
        }
    }
    
    // Intercept Macro Analysis button
    const topicBtn = e.target.closest('#topicButton');
    if (topicBtn && !window.currentUser) {
        e.preventDefault();
        e.stopPropagation();
        window.requireAuthentication('Macro Analysis', () => {
            topicBtn.click(); // re-trigger safely
        });
    }
    
    // Intercept Battle Mode button
    const battleBtn = e.target.closest('#battleButton');
    if (battleBtn && !window.currentUser) {
        e.preventDefault();
        e.stopPropagation();
        window.requireAuthentication('Battle Mode', () => {
            battleBtn.click(); // re-trigger safely
        });
    }
}, true); // Use capture phase to intercept before script.js handles it!

document.addEventListener('focusin', (e) => {
    if ((e.target.id === 'topicInput' || e.target.id === 'topicInputA' || e.target.id === 'topicInputB') && !window.currentUser) {
        e.target.blur();
        window.requireAuthentication('Macro Analysis', () => {
            e.target.focus();
        });
    }
}, true);

// Initialization and State Check
async function initAuth() {
    try {
        // Step 1: Check if we just returned from an OAuth provider (Google/Facebook)
        const params = new URLSearchParams(window.location.search);
        const hashParams = new URLSearchParams(window.location.hash.replace('#', ''));
        
        const code = params.get('insforge_code') || params.get('code');
        const accessToken = hashParams.get('access_token') || params.get('access_token');
        
        if (code) {
            // PKCE flow: exchange the code for a session
            console.log('OAuth code detected, exchanging for session...');
            try {
                const { data, error } = await supabase.auth.exchangeCodeForSession(code);
                if (!error && data?.session) {
                    window.currentUser = data.session.user;
                    // Clean the URL so the code doesn't linger in the address bar
                    window.history.replaceState({}, document.title, '/');
                }
            } catch (exchangeErr) {
                console.warn('Code exchange failed, trying getSession fallback:', exchangeErr);
            }
        } else if (accessToken) {
            // Implicit flow: SDK may auto-handle, just get session
            console.log('OAuth access_token detected in URL...');
            window.history.replaceState({}, document.title, '/');
        }
        
        // Step 2: Always do a final getSession to confirm current state
        if (!window.currentUser) {
            const { data: { session }, error } = await supabase.auth.getSession();
            if (!error) window.currentUser = session?.user || null;
        }
        
    } catch (err) {
        console.error("Auth init failed:", err);
        window.currentUser = null;
    }
    
    updateUIAuthStatus();

    // Listen for future auth changes (e.g., token refresh, logout)
    supabase.auth.onAuthStateChange((event, session) => {
        window.currentUser = session?.user || null;
        updateUIAuthStatus();
    });
}

function updateUIAuthStatus() {
    const authSection = document.getElementById('auth-section');
    const userProfileSection = document.getElementById('user-profile-section');
    const navUserEmail = document.getElementById('nav-user-email');
    const overlay = document.getElementById('macro-auth-overlay');
    
    if (window.currentUser) {
        console.log("Authenticated as:", window.currentUser.email);
        
        // Close the login overlay with a smooth fade-out
        if (overlay && !overlay.classList.contains('hidden')) {
            overlay.classList.remove('opacity-100');
            overlay.style.pointerEvents = 'none';
            setTimeout(() => overlay.classList.add('hidden'), 500);
        } else if (overlay) {
            overlay.classList.add('hidden');
            overlay.style.pointerEvents = 'none';
        }
        
        // Swap Login button → Profile picture
        if (authSection) authSection.style.display = 'none';
        if (userProfileSection) userProfileSection.style.display = 'flex';
        
        // Populate avatar or fallback
        const avatarUrl = window.currentUser.user_metadata?.avatar_url || window.currentUser.user_metadata?.picture;
        const navUserAvatar = document.getElementById('nav-user-avatar');
        const navUserInitials = document.getElementById('nav-user-initials');
        
        if (avatarUrl && navUserAvatar) {
            navUserAvatar.src = avatarUrl;
            navUserAvatar.style.display = 'block';
            if (navUserInitials) navUserInitials.style.display = 'none';
        } else {
            // Fallback: show initials from email
            if (navUserAvatar) navUserAvatar.style.display = 'none';
            if (navUserInitials) {
                const email = window.currentUser.email || '';
                navUserInitials.innerText = email.charAt(0).toUpperCase();
                navUserInitials.style.display = 'flex';
            }
        }
        
        // Always show email in dropdown
        if (navUserEmail) navUserEmail.innerText = window.currentUser.email || '';
        
        const role = window.currentUser.user_metadata?.role || 'USER';
        if (role === 'ADMIN' && typeof window.loadAdminDashboard === 'function') {
            document.getElementById('admin-dashboard')?.classList.remove('hidden');
        }
        
        // Execute pending action (e.g., re-focus search bar or re-run analysis)
        if (window.intendedAuthAction) {
            const action = window.intendedAuthAction;
            window.intendedAuthAction = null;
            setTimeout(action, 600); // wait for overlay fade-out
        }
        
    } else {
        // Logged out — show Login button, hide profile
        if (authSection) authSection.style.display = 'flex';
        if (userProfileSection) userProfileSection.style.display = 'none';
        if (overlay) {
            overlay.classList.add('hidden');
            overlay.style.pointerEvents = 'none';
        }
    }
}

async function logout() {
    try {
        await supabase.auth.signOut();
        window.currentUser = null;
        window.location.reload();
    } catch (e) {
        console.error("Logout failed", e);
    }
}
window.logout = logout;

document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    
    const btnGoogle = document.getElementById('auth-google-btn');
    const btnFacebook = document.getElementById('auth-facebook-btn');
    const btnSignup = document.getElementById('auth-signup-btn');
    const btnLogin = document.getElementById('auth-login-btn');
    
    if (btnGoogle) {
        btnGoogle.addEventListener('click', async (e) => {
            e.preventDefault();
            btnGoogle.innerHTML = 'Connecting to Google...';
            btnGoogle.disabled = true;
            try {
                const { data, error } = await supabase.auth.signInWithOAuth({ 
                    provider: 'google',
                    options: {
                        redirectTo: window.location.origin
                    }
                });
                if (error) throw error;
            } catch (err) {
                console.error("OAuth error:", err);
                const errorMsg = err.message || err.error_description || "Unknown error";
                alert("Google sign-in could not be completed: " + errorMsg);
                btnGoogle.innerHTML = '<i class="fa-brands fa-google text-xl"></i> Continue with Google';
                btnGoogle.disabled = false;
            }
        });
    }
    
    if (btnFacebook) {
        btnFacebook.addEventListener('click', async (e) => {
            e.preventDefault();
            btnFacebook.innerHTML = 'Connecting to Facebook...';
            btnFacebook.disabled = true;
            try {
                const { data, error } = await supabase.auth.signInWithOAuth({ 
                    provider: 'facebook',
                    options: {
                        redirectTo: window.location.origin
                    }
                });
                if (error) throw error;
            } catch (err) {
                console.error("OAuth error:", err);
                const errorMsg = err.message || err.error_description || "Unknown error";
                alert("Facebook sign-in could not be completed: " + errorMsg);
                btnFacebook.innerHTML = '<i class="fa-brands fa-facebook text-xl"></i> Continue with Facebook';
                btnFacebook.disabled = false;
            }
        });
    }
    
    if (btnSignup) {
        btnSignup.addEventListener('click', async () => {
            const email = document.getElementById('auth-email').value;
            const password = document.getElementById('auth-password').value;
            if (!email || !password) return alert("Enter email and password.");
            
            btnSignup.innerText = "Signing up...";
            btnSignup.disabled = true;
            
            try {
                const { data, error } = await supabase.auth.signUp({ 
                    email, 
                    password,
                    options: {
                        data: { name: email.split('@')[0], role: email === 'sentio1508@gmail.com' ? 'ADMIN' : 'USER' }
                    }
                });
                
                if (error) alert("Signup Error: " + error.message);
                else alert("Signup successful! You can now log in.");
            } catch (err) {
                alert("Network error during signup.");
            }
            
            btnSignup.innerText = "Sign Up";
            btnSignup.disabled = false;
        });
    }
    
    if (btnLogin) {
        btnLogin.addEventListener('click', async () => {
            const email = document.getElementById('auth-email').value;
            const password = document.getElementById('auth-password').value;
            if (!email || !password) return alert("Enter email and password.");
            
            btnLogin.innerText = "Logging in...";
            btnLogin.disabled = true;
            
            try {
                const { data, error } = await supabase.auth.signInWithPassword({ email, password });
                if (error) {
                    alert("Login Error: " + error.message);
                } else {
                    window.currentUser = data.user;
                    updateUIAuthStatus();
                }
            } catch (err) {
                alert("Network error during login.");
            }
            
            btnLogin.innerText = "Log In";
            btnLogin.disabled = false;
        });
    }
    
    // Check for Auth Errors from redirects
    const urlParams = new URLSearchParams(window.location.search);
    const errorParam = urlParams.get('error');
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const errorHash = hashParams.get('error_description');
    
    if (errorParam || errorHash) {
        let msg = "Google sign-in could not be completed. Please try again.";
        if (errorParam === 'oauth_not_configured') msg = "Login unavailable: OAuth provider is not configured on the backend.";
        else if (errorParam === 'oauth_provider_unavailable') msg = "The OAuth provider is currently unavailable.";
        else if (errorParam === 'oauth_provider_denied') msg = "OAuth login was cancelled or denied.";
        else if (errorParam === 'oauth_invalid_callback') msg = "Invalid callback received from the provider.";
        else if (errorParam === 'oauth_session_missing') msg = "Failed to establish a session after OAuth.";
        else if (errorParam === 'account_deactivated') msg = "Your account has been deactivated.";
        
        const overlay = document.getElementById('macro-auth-overlay');
        if (overlay) {
            overlay.classList.remove('hidden');
            overlay.classList.add('opacity-100');
            overlay.style.pointerEvents = 'auto';
            const desc = overlay.querySelector('p');
            const title = overlay.querySelector('h3');
            if (title) title.innerText = "Authentication Failed";
            if (desc) desc.innerText = msg;
        } else {
            alert(msg);
        }
        
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});
