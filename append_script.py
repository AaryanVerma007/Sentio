# append_script.py

content_to_append = """

// ==========================================
// 19. SHADER AND GRID ANIMATIONS (STITCH DESIGN)
// ==========================================

// Shader Background Implementation
const initShader = () => {
    const container = document.getElementById('shader-container');
    if (!container) return;

    if (typeof THREE === 'undefined') {
        console.warn('THREE.js not loaded, skipping shader');
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    const renderer = new THREE.WebGLRenderer({ alpha: false });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const vertexShader = `
        varying vec2 v_texCoord;
        void main() {
            v_texCoord = uv;
            gl_Position = vec4(position, 1.0);
        }
    `;

    const fragmentShader = `
        precision highp float;
        varying vec2 v_texCoord;
        uniform float u_time;
        uniform vec2 u_resolution;
        uniform vec2 u_mouse;

        float noise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        float smoothNoise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            float a = noise(i);
            float b = noise(i + vec2(1.0, 0.0));
            float c = noise(i + vec2(0.0, 1.0));
            float d = noise(i + vec2(1.0, 1.0));
            return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
        }

        float fbm(vec2 p) {
            float v = 0.0;
            float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * smoothNoise(p);
                p *= 2.0;
                a *= 0.5;
            }
            return v;
        }

        void main() {
            vec2 uv = v_texCoord;
            vec2 mouse = u_mouse / u_resolution;
            
            // Create a sense of depth and movement
            float n = fbm(uv * 3.0 + u_time * 0.05);
            n += fbm(uv * 6.0 - u_time * 0.1) * 0.5;
            
            // Add mouse interaction
            float dist = distance(uv, mouse);
            float mouseEffect = smoothstep(0.4, 0.0, dist) * 0.2;
            
            // Primary color from Sentiment Noir (#00f2ff converted to vec3)
            vec3 color1 = vec3(0.0, 0.95, 1.0); 
            vec3 color2 = vec3(0.02, 0.04, 0.05); // Deep background
            
            vec3 finalColor = mix(color2, color1, n * 0.15 + mouseEffect);
            
            // Add "digital grain" or data points
            float grain = noise(uv * 500.0 + u_time);
            if (grain > 0.98) finalColor += color1 * 0.3;

            gl_FragColor = vec4(finalColor, 1.0);
        }
    `;

    const uniforms = {
        u_time: { value: 0 },
        u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        u_mouse: { value: new THREE.Vector2(0, 0) }
    };

    const material = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms,
        depthWrite: false,
        depthTest: false
    });

    const geometry = new THREE.PlaneGeometry(2, 2);
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;

    document.addEventListener('mousemove', (e) => {
        targetMouseX = e.clientX;
        targetMouseY = window.innerHeight - e.clientY; // Invert Y for shader
    });

    const animate = (time) => {
        requestAnimationFrame(animate);
        
        // Smooth mouse interpolation
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        uniforms.u_time.value = time * 0.001;
        uniforms.u_mouse.value.set(mouseX, mouseY);
        
        renderer.render(scene, camera);
    };

    animate(0);

    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        uniforms.u_resolution.value.set(window.innerWidth, window.innerHeight);
    });
};

// Interactive Grid Effect
const initGrid = () => {
    const grid = document.getElementById('interactive-grid');
    if(!grid) return;
    
    document.addEventListener('mousemove', e => {
        const rect = grid.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        grid.style.setProperty('--mouse-x', `${x}px`);
        grid.style.setProperty('--mouse-y', `${y}px`);
        grid.classList.add('active'); // active class for opacity
    });
};

// Scroll Reveal Observer
const initReveal = () => {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('reveal-hidden');
                entry.target.classList.add('reveal-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-item').forEach(item => {
        observer.observe(item);
    });
};

// Simple subtle parallax for hero particles
const initParallax = () => {
    const hero = document.querySelector('.hero-particle-bg > div');
    document.addEventListener('mousemove', (e) => {
        if(!hero) return;
        const x = (e.clientX / window.innerWidth - 0.5) * 30;
        const y = (e.clientY / window.innerHeight - 0.5) * 30;
        hero.style.transform = `translate(${x}px, ${y}px)`;
    });
};

window.addEventListener('DOMContentLoaded', () => {
    initShader();
    initGrid();
    initReveal();
    initParallax();
});
"""

with open('script.js', 'a', encoding='utf-8') as f:
    f.write(content_to_append)
