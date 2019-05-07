This module moves Javascript assets to the bottom of the page (below the fold)
preventing your website having render-blocking Javascript.

When a visitor enters your website the browser will parse the HTML result.
Whenever the parser encounters a script, it has to load and execute the script before it can continue parsing.
So with render-blocking Javascript (e.g. in the head tag) the time to render the above the fold content increases.

Without render-blocking Javascript (by e.g. loading it below the fold) the page first render occurs faster.
This may result in various benefits e.g. lower bounce rate.

More information:

* `Render-blocking Javascript <https://developers.google.com/speed/docs/insights/BlockingJS>`_
* `Above the fold <https://en.wikipedia.org/wiki/Above_the_fold>`_
