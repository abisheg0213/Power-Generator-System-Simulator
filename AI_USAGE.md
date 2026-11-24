# AI Usage

I used Cursor in agent mode for this project, and it made the work faster and easier to follow.

**Graphs.** I used it to build the frequency plot with the 49.50 Hz and 50.50 Hz limit lines, and the generator and breaker state plots as step graphs. When a graph looked wrong, I described what I saw, and it helped me find the cause.

**Understanding the physical process.** I used it to make sense of the generator, breaker and frequency relationship. It helped me see that frequency is the balance between generation and load, and it helped me work out the thresholds for opening and closing the breaker.

**Fixing bugs.** It found and fixed small syntax and logic errors in my code, such as an invalid `!` operator and a control rule that only ran inside one branch. It also pointed out a floating-point rounding issue that made a threshold trigger one second late.

**Speed.** Working with it was much faster than working alone. I could try an idea, run it, look at the result, and adjust.

I did not accept its output without checking. I ran every change, compared the results with the graphs and the brief, and kept only what worked.
