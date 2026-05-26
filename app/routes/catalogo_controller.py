from playwright.sync_api import sync_playwright
from fastapi.responses import FileResponse
from fastapi import APIRouter

app = APIRouter(
    tags=["Catalogo"]
)


@app.get("/pdf")
def generar_pdf():

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()
        
        page.goto(
            "http://localhost:5173/catalogoPDF"
        )

        page.wait_for_selector(
            ".catalogo-card"
        )

        page.wait_for_load_state(
            "networkidle"
        )

        page.wait_for_timeout(5000)

        page.pdf(
            path="catalogoPDF.pdf",
            format="A4",
            print_background=True
        )

        browser.close()

    return FileResponse(
        "catalogoPDF.pdf",
        media_type="application/pdf",
        filename="catalogoPDF.pdf"
    )