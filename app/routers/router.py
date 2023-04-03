
from fastapi.routing import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from services.AnalysisService import AnalysisService

router = APIRouter()
templates = Jinja2Templates(directory='templates')
analysis_service = AnalysisService(os.environ.get('DATA_JOB_SERVICE'))

@router.get('/', response_class=HTMLResponse)
def get_index(request: Request) -> HTMLResponse:
    try:
        return templates.TemplateResponse('index.html', {'request': request})
    except Exception as e:
        return HTMLResponse(content=f'Error: {e}', status_code=500)

@router.post('/request_analysis')
async def request_analysis(request: Request):
    try:
        form = await request.form()
        marketplace = form['marketplace']
        search_query = form['search_query']
        analysis_service.submit_analysis_request(marketplace, search_query)
        print(f'Redirecting to /{marketplace}/{search_query}')
        return RedirectResponse(url=f'/{marketplace}/{search_query}', status_code=303)
    except Exception as e:
        return HTMLResponse(content=f'Error: {e}', status_code=500)
    

@router.get('/{marketplace}/{search_query}', response_class=HTMLResponse)
def get_analysis(request: Request, marketplace: str, search_query: str) -> HTMLResponse:
    print(f'Getting analysis for {marketplace} and {search_query}')
    try:
        analysis = analysis_service.get_analysis(marketplace, search_query)
        return templates.TemplateResponse('analysis.html', {'request': request, 'analysis': analysis})
    except Exception as e:
        return HTMLResponse(content=f'Error: {e}', status_code=500)
