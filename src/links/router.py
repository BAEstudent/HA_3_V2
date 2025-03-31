from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from database import get_async_session

from links.models import links
from links.shemas import LinkCreate

from datetime import datetime
import uuid

def create_short_url():
    return uuid.uuid4().hex[:6] + datetime.now().strftime("%S%f")[:-3]


router = APIRouter(
    prefix="/links",
    tags=["Links"]
)

@router.get("/")
async def get_short_code(short_code: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(links).where(links.c.short_code == short_code)
        result = await session.execute(query)
        result_json = result.mappings().all()[0]

        num = result_json['num_queries']
        statement = update(links).where(links.c.short_code == short_code).values({
            links.c.num_queries: num+1,
            links.c.last_queried_dt: datetime.now() #.strftime("%y-%m-%d %H-%M-%S.%f")[:-3]
            })
        await session.execute(statement)
        await session.commit()

        return RedirectResponse(result_json['long_url'])
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.post("/")
async def shorten(long_url: str, session: AsyncSession = Depends(get_async_session)):
    try:
        statement = insert(links).values({
            links.c.long_url: long_url,
            links.c.short_code: create_short_url(),
            links.c.create_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
            links.c.last_queried_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
            links.c.num_queries: 0
        })
        await session.execute(statement)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.delete("/")
async def delete_link(short_code: str, session: AsyncSession = Depends(get_async_session)):
    try:
        statement = delete(links).where(links.c.short_code == short_code)
        await session.execute(statement)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.put("/")
async def update_link(short_code: str, session: AsyncSession = Depends(get_async_session)):
    try:
        new_short_code = create_short_url()
        statement = update(links).where(links.c.short_code == short_code).values({
            links.c.short_code: new_short_code,
            links.c.create_dt: datetime.now().strftime("%y-%m-%d %H-%M-%S.%f")[:-4]
            })
        await session.execute(statement)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.get("/{short_code}/stats")
async def get_link_stats(short_code: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(links).where(links.c.short_code == short_code)
        result = await session.execute(query)
        result_json = result.mappings().all()[0]

        return {"status": "success",
                "data": {
                    "long_url": result_json['long_url'],
                    "create_dt": result_json['create_dt'],
                    "last_queried_dt": result_json['last_queried_dt'],
                    "num_queries": result_json['num_queries']
                }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.post("/{custom_alias}")
async def shorten_lias(long_url: str, custom_alias: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(links)
        result = await session.execute(query)
        result_list = result.mappings().all()
        used_short_codes = [x['short_code'] for x in result_list]

        if custom_alias not in used_short_codes:
            statement = insert(links).values({
                links.c.long_url: long_url,
                links.c.short_code: custom_alias,
                links.c.create_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
                links.c.last_queried_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
                links.c.num_queries: 0
            })
            await session.execute(statement)
            await session.commit()
            return {"status": "success"}
        else:
            raise Exception("Sorry, alias already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

def delete_on_expiration():
    statement = delete(links).where(links.c.expiration_dt < datetime.now())
    await session.execute(statement)
    await session.commit()


@router.post("/{expire_at}")
async def shorten_lias(long_url: str, expire_at: str, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(links)
        result = await session.execute(query)
        result_list = result.mappings().all()
        used_short_codes = [x['short_code'] for x in result_list]

        if custom_alias not in used_short_codes:
            statement = insert(links).values({
                links.c.long_url: long_url,
                links.c.short_code: custom_alias,
                links.c.create_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
                links.c.last_queried_dt: datetime.now(), #.strftime("%y-%m-%d %H-%M-%S.%f")[:-4],
                links.c.expire_dt: expire_at,
                links.c.num_queries: 0
            })
            await session.execute(statement)
            await session.commit()
            background_tasks.add_task(delete_on_expiration)
            return {"status": "success"}
        else:
            raise Exception("Sorry, alias already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })
    

@router.get("/search")
async def get_link_stats(original_url: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(links).where(links.c.long_url == original_url)
        result = await session.execute(query)
        result_json = result.mappings().all()[0]

        return {
            "status": "success",
            "data": {"short_code": result_json['short_code']}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": e
        })