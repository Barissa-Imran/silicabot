import os
import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()

router = routing.Router()

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})

# @router.register("issue_comment", action="created") #changes=""
# async def issue_claim_event(event, gh, *args, **kwargs):
#     """
#     Assign issues to users when called upon
#     """
#     url = event.data["issue"]
#     author = event.data["issue"]["user"]["login"]

#     label = "in progress"



# Main coroutine
@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    # Authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    # representantion of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    # GitHub API session start
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "Barissa-Imran",
                                    oauth_token=oauth_token)

        # callback for the event
        await router.dispatch(event, gh)
    
    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)