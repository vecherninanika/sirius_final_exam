from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import select, update, delete

from webapp.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema import *

ingredient_router = APIRouter(prefix='/ingredient')


@ingredient_router.get(
    '/read',
    response_model=IngredientResponse,
)
async def read_ingredient(
    body: IngredientData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    ingredient = (await session.scalars(select(Ingredient).where(Ingredient.title == body.title))).one_or_none()

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient "{body.title}" does not exist')

    return ORJSONResponse({'id': ingredient.id, 'title': ingredient.title})


@ingredient_router.post(
    '/create',
    response_model=IngredientResponse,
)
async def create_ingredient(body: IngredientData, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    async with session.begin_nested():
        async with session.begin_nested():
            data_dict = body.dict()
            ingredient = Ingredient(**data_dict)
            session.add(ingredient)
            await session.flush()
            await session.commit()

    return ORJSONResponse({"id": ingredient.id, "title": ingredient.title})


@ingredient_router.post(
    '/update/{ingredient_id}',
    response_model=IngredientResponse,
)
async def update_ingredient(
    ingredient_id: int, body: IngredientData, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    data = body.dict()
    await session.execute(update(Ingredient).where(Ingredient.id == ingredient_id).values(**data))
    updated = (await session.scalars(select(Ingredient).where(Ingredient.id == ingredient_id))).one_or_none()
    await session.commit()

    if updated.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient "{body.title}" does not exist')

    return ORJSONResponse({'id': updated.id, 'title': updated.title})


@ingredient_router.post(
    '/delete/{ingredient_id}',
    response_model=IngredientData,
)
async def delete_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    deleted_id = (
        await session.execute(delete(Ingredient).where(Ingredient.id == ingredient_id).returning(Ingredient.id))
    ).one_or_none()[0]
    await session.commit()

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient does not exist')

    return ORJSONResponse({'id': deleted_id})
