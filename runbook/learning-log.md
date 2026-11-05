# TERRY'S LEARNING LOG

Plain-English lessons from the work we do together. Each one is short. Reread them
any time. New ones get added at the bottom as they come up.

---

## 1. The page you edit and the machine that writes the page

**The comparison:** a bakery's recipe card versus the loaf. If you fix the loaf, the
next batch comes out the old way. Fix the card and every loaf is right.

**What it means here:** most pages on our sites are written by a program every
half hour from a set of instructions (`wire.py` on Newswire, `render_site.py` on
Gospel). Those are the recipe cards. The `.html` files are the loaves.

**What went wrong:** on the CDC pages I fixed the loaf. Thirty minutes later the
program baked a fresh one and my fix vanished. The fix has to go into the recipe.

**The word:** *source* is the recipe. *Output* or *generated* is the loaf.

## 2. Draft versus live: branches and main

**The comparison:** a Word document you are still editing versus the one you have
sent to the printer.

**What it means here:** a *branch* is a private draft copy of the whole site. *main*
is the published version, the only one the world sees. *Merging* is sending the
draft to the printer. That is why we could show you the Freda Payne review privately
and only publish it when you said go.

## 3. Why a photo gets its face cut off

**The comparison:** a tall picture pushed into a wide frame, like fitting a portrait
into a letterbox. Something has to be trimmed.

**What it means here:** the front page shows photos in a wide banner and trims from
the middle. Her face was near the top, so it went. The fix was a wide crop with her
face inside it, plus a setting called a *focal point* that says which part of the
photo to protect.

**The word:** *cropping* is trimming a picture to fit a frame. `object-fit: cover`
is the instruction that says fill the frame and trim the rest.

## 4. Linking to a photo versus copying it

**The comparison:** pointing at a painting in a museum versus taking it home.

**What it means here:** for wire stories we point at the publisher's own photo and
print their name under it. We do not copy it onto our server. That keeps us on the
right side of copyright, and it is why every wire photo now says "Photo: [outlet]".
The word for pointing at someone else's file is *hotlinking*.

## 5. Telling Google and Bing you exist

**The comparison:** handing the post office a change-of-address card instead of
waiting for the mail to find you.

**What it means here:** a *sitemap* is a list of every page on your site, handed to
search engines. A *news sitemap* is the same list for fresh stories only, which is
what Google News reads. *IndexNow* is a shortcut that tells Bing and others the
moment a page changes. None of these can promise a ranking. They only make sure
you are found.

## 6. Testing with a pretend internet

**The comparison:** a fire drill. You practise with a fake fire so the real one goes
right.

**What it means here:** my workspace cannot reach the live internet. So when I wrote
the code that hunts for missing photos, I tested it against a pretend internet that
I controlled, with a good page, a bare page and a YouTube link. It passed every case
before it ever touched a real website. That is called a *test with a stand-in*, or
a *mock*.

## 7. Two kinds of robots read your website

**The comparison:** a librarian versus a ghostwriter. The librarian reads your book so
she can send readers to it. The ghostwriter reads it to learn your style and write
his own.

**What it means here:** AI companies send two kinds of crawlers (robots that read
websites). A *search crawler*, like ChatGPT's OAI-SearchBot, reads our stories so it
can quote them and link back to us; that brings readers. A *training crawler* reads
them to teach an AI model; that brings nothing unless we're paid. A small file on
each site called robots.txt tells each robot "come in" or "stay out." We let the
librarians in and keep the ghostwriters out until someone pays for our archive.

## The doorman (robots.txt)
Every site has a small file called robots.txt. Think of it as the doorman's list: it tells search engines and AI robots which doors are open. We wrote ChatGPT's, Perplexity's and Claude's search robots onto the list by name, so when someone asks an AI a question, our stories can be read, quoted and linked. Without the list, some robots stay polite and walk away.

## Nov 4, 2026 — Search Console is the front door to Google

The websites were built for Google but never formally introduced. Search Console is the introduction: you prove you own the site (a small file Google gives you, placed on the site), then hand Google the sitemap, which is the table of contents. After that Google reads every new story on its own, and Search Console shows what people searched to find us. One file can verify several sites when the same Google account owns them, which is why HNA and HTA verified in a minute.

## Nov 5, 2026 — The key and the lock

The social auto-poster works like a valet: Meta gave our app a key (the access token) that can only do the jobs Terry approved, which are posting to his Pages and Instagram. The key lives in GitHub Secrets, a locked box the robot can open but nobody can read, not even in the code. Never paste a key into chat or a screenshot: anyone holding it can post as the brand until it is replaced.

## Media alert vs. press release (Nov 5, 2026 — AGFF 2026)
A media alert is an invitation for reporters: who, what, when, where, photo moments, how to get credentials. It goes out the day before or the morning of an event, because assignment desks plan their crews then. A press release is a finished story, and its best moment is after the event (the winners release). Sending a long release the night before gets skimmed and skipped; the alert gets a camera crew sent.
## Nov 5, 2026 — A web page can't keep a sign-up sheet by itself

Our sites are like printed posters: anyone can read them, but nobody can write on them. So a registration form needs a mail carrier, a small free service (FormSubmit) that takes what someone typed and emails it to the inbox. The first time it's used, it emails a one-time "Activate" button to the inbox owner. Until that's clicked, registrations go nowhere.

## Nov 5, 2026 — A homepage that cleans itself
Terry's rule: old stories don't sit on the front page. wire.py now has one number, HOME_OURS_DAYS = 5. Our stories ride the homepage for five days after their date, then step off on their own and live on their section page, same link. Like a shop window that changes itself every few days, while the stockroom keeps everything. Without it, a September story (Freda Payne) was still in the window in November.

## Nov 5, 2026 — The supplier wins, not the gold miner
In a gold rush the people who sold shovels got rich more reliably than the miners. Goldman Sachs says only about 4% of creators earn over $100K a year, but the agencies around them (Whalar, about $110M revenue) keep a slice of every deal. That slice is called margin: the gap between what the brand pays and what the creator gets. PR STARPOWER's play is to be the shovel seller: access, deals and paperwork, with a written term sheet every time we give something away.
