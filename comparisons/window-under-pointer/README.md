# Window Under Pointer

## Running

```sh-session
$ cd path/to/this/directory
$ ./window-under-pointer
```

[The included `R` script](process_data.R) is what I used to generate the stuff below.

## Included

I ran a quick sample of 10000 clicks per library. `Xlib` was phenomenally faster (although we're really talking fractions of a millisecond here).

![Gather Basics Time](output/violin/gather_basics.png)
![Root Window Time](output/violin/root_window.png)
![Window Under Pointer Time](output/violin/recursion.png)
![Get Window Name Time](output/violin/get_names.png)
![Parse Window Name Time](output/violin/parse_names.png)
![Exit Time](output/violin/exit.png)
![Total Time](output/violin/total.png)

## Click Map

For grins, I built this too.

![Scatterplot of Clicks](output/clicks.png)
