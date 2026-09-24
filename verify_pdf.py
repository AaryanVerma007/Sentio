import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        file_path = os.path.abspath('test_pdf.html')
        await page.goto(f"file://{file_path}")
        
        print("Exporting PDF...")
        async with page.expect_download(timeout=60000) as download_info:
            await page.click("button")
        
        download = await download_info.value
        await download.save_as("test_output.pdf")
        print("PDF saved as test_output.pdf")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
