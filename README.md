# Trencher

> noun
> 
> 1. _historical_ a wooden plate or platter for food

## Wait, what?

Trencher is a Django project I threw together to take some of the hassle out of our regular grocery shopping.
When the time comes to plan out our grocery shopping for the week (or however long it is), we can pick out the meals we’d like to eat, and Trencher can automatically figure out what ingredients we might need and populate our grocery list.
As we eat the meals, we can tick them off the list.

## Cool! Can I run this myself?

You’re welcome to have a go.

I started this project to solve my immediate problem of planning out a grocery order, when we don’t own a car, during a pandemic.
If anyone else finds it useful to poke around with, that’s a nice bonus.
As such, I haven’t put a whole lot of thought or effort into letting people swap out their own technologies.
I’m running this on:

* [Fly][], because Heroku decided to shut down their free tier
* Postgres, because MySQL has bitten me one too many times
* [Todoist][], because it’s the best to-do app I’ve found for my needs since [Microsoft shut down Wunderlist][wunderlist]

If you want to use different tech, that’s perfectly fine, but you’ll probably need to write your own code, and the structure of the app might not make it easy.

[Fly]: https://fly.io/
[Todoist]: https://todoist.com/
[wunderlist]: https://www.cnet.com/news/microsoft-to-replace-wunderlist-with-to-do-in-may-2020/

Most of the customisation comes from environment variables, either through your platform's built-in mechanisms or configured manually.
The app knows about:

* `DATABASE_URL`
* `SECRET_KEY`
* `TODOIST_ACCESS_TOKEN`
* `TODOIST_PROJECT_ID`
* `HONEYCOMB_API_KEY`
* `HONEYCOMB_DATASET`

If you don’t fancy setting up [Honeycomb][] for tracing data, you should be able to leave those environment variables unset, and Trencher should continue without them. I haven’t tested that recently, though, so no promises.

[django-heroku]: https://pypi.org/project/django-heroku/
[Honeycomb]: https://www.honeycomb.io

## Hey, this isn’t production-level code!

Correct.
This isn’t a production-level project.