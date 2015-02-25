# See wiki for software needed for image processing tasks 

# command for examining `FITS` header 
```sh
$ head -1 'FITSNAME' | fold -s -w 80
```

# uncompressing `.fz` files 
more documentation [here](http://archive.noao.edu/doc/SDM_fpack_usernotes.html)
```
$ funpack stuff.fits.fz
```


# WCS coordinates for cropping the image 
Crop only the region showed in the [van Weeren et al. 2012
paper](http://arXiv.org/1206.2294) 


Location           | SEX RA | SEX DEC | WCS RA | WCS DEC 
-------------------|--------|---------|--------|-----------------
Lower left corner  | 17:52:25 | 44:37:00 | 268.10416666666663 | 44.61666666666667
Upper right corner | 17:51:48 | 44:43:30 | 267.95 | 44.770833   

```sh
$ ftcopy 'I.fits[5608:8358, 5812:8561]' \!I_cropped.fits
$ ftcopy 'R.fits[5599:8358, 5812:8561]' \!R_cropped.fits chatter=5
$ ftcopy 'G.fits[5608:8358, 5812:8561]' \!G_cropped.fits chatter=5
```
 
|band | PIX X | PIX Y |  position | 
|----|-----|------|--------|--------|
|I | 5608.2866 | 5812.1494 | lower left | 
|I | 8357.5158 | 8561.3786 | upper right| 
|R | 5599.3701 | 5812.1494 | lower left | 
|R | 8357.5158 | 8561.3728 | upper right| 
|G | 5608.2866 | 5812.1494 | lower left | 
|G | 8357.5158 | 8561.3728 | upper right| 
