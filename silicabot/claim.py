import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()

router = routing.Router()


@router.register("issue_comment", action="created") #changes=""
async def issue_claim_event(event, gh, *args, **kwargs):
    """
    Assign issues to users when called upon
    """
    issue_url = event.data["issue"]["url"]
    label_url = event.data["issue"]["labels_url"]
    author = event.data["comment"]["user"]["login"]

    # comment = event.data["comment"]
    comment = event.data["comment"]["body"]
    call = "@savannahbot claim"
    uncall = "@savannahbot unclaim"

    assignees_url = event.data["issue"]["assignees"]

    print(assignees_url)

    if comment == call:
        # Assign
        await gh.post(issue_url["assignees"], data=[author,])
    elif comment == uncall:
        # Unassign
        await gh.DELETE(issue_url["assignees"], data=[author])
    pass

    # label = "in progress"