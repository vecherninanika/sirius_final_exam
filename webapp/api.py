from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import select, update, delete

from webapp.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient


ingredient_router = APIRouter(prefix='/ingredient')


@ingredient_router.get('/read')
async def read_ingredient(
    body,
    session = Depends(get_session),
) -> ORJSONResponse:
    ingredient = (await session.scalars(select(Ingredient).where(Ingredient.title == body.title))).one_or_none()

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient "{body.title}" does not exist')

    return ORJSONResponse({'id': ingredient.id, 'title': ingredient.title})


@ingredient_router.post('/create')
async def create_ingredient(body, session = Depends(get_session)) -> ORJSONResponse:

    async with session.begin_nested():
        async with session.begin_nested():
            ingredient = Ingredient(**body)
            session.add(ingredient)
            await session.flush()
            await session.commit()

    return ORJSONResponse({"id": ingredient.id, "title": ingredient.title})


@ingredient_router.post('/update/{ingredient_id}')
async def update_ingredient(
    ingredient_id: int, body, session = Depends(get_session)
) -> ORJSONResponse:
    
    await session.execute(update(Ingredient).where(Ingredient.id == ingredient_id).values(**body))
    updated = (await session.scalars(select(Ingredient).where(Ingredient.id == ingredient_id))).one_or_none()
    await session.commit()

    if updated.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient "{body.title}" does not exist')

    return ORJSONResponse({'id': updated.id, 'title': updated.title})


@ingredient_router.post('/delete/{ingredient_id}')
async def delete_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    deleted_id = (
        await session.execute(delete(Ingredient).where(Ingredient.id == ingredient_id).returning(Ingredient.id))
    ).one_or_none()[0]
    await session.commit()

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient does not exist')

    return ORJSONResponse({'id': deleted_id})
