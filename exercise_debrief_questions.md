Exercise 1:

What did you notice about the level of detail in the lock file? 

That is what it takes to create reproducible environments. A simple requirements.txt or environment.yml is not going to cut it, especially if you have to curate it manually.

Anybody have an idea about why the uv environment build faster the second time?

Caching. And it would have been less than 1 second if we were working locally instead of in the codespaces environment that keeps our workspace on a different filesystem than where uv puts the cache.

Exercise 2:

We could have written the `growth_rate` function to return the value as a percentage. Why is it better to not do that?

Because percentage is a REPRESENTATION, it's not the real value. So it belongs in a format specifier, not in the data itself

Why is it wrong to add a line as an f-string w/o changing the first line?
Because the code should match. They should either both use .format or both use f-string

Do you want to write tag functions?
No. You want to be able to use t-strings for safety. But you don't want to have to validation them with tag functions. Stay aware of whether the libraries you use accept t-strings. We had to use a beta version of sqlalchemy in the example to get it to work. And we couldn't rely on sqlite natively, because t-strings aren't supported there yet.

Exercise 3:
Who got a mix of \ and / in their paths? Anybody figure out how to fix it?
Pure paths vs. Paths. - If it doesn't touch the file system (like the first question), you can use a pure path. This is Windows, so `PureWindowsPath`. Then you get the right mix.

Who wants to use `write_text` to append a new row to the file? Anybody want to guess why that's a bad idea?

`write_text` overwrites. Really great if that's what you want. Bad if you want to append. These are convenience methods designed to handle only the most common use cases, not to be comprehensive replacements for `open`.

Would `with_suffix` have worked if the file didn't actually exist in the file system? 

Yes - it's a pure path manipulation

Would -rename` have worked if the file didn't actually exist in the file system?

No - it touches the file system to rename.

Exercise 4:

What's the difference in terms of where the values are coming from between the first case where we instantiate the model directly and the second case where we use `model_validate`?

First case we have individual variables. Second case we have a dictionary of values. That matters. If you already have a dictionary, use `model_validate`. If you have json, use `model_validate_json`. There's a reason we use `DictReader` here.