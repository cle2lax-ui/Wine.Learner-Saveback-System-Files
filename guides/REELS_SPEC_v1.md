# Reels Spec — v1

A distribution treatment, not a series. Two per week, assembled from
arc content already built and already reviewed.

## Canvas

**1080 × 1920, 9:16.** Vertical content is re-composed on this canvas
from source content. It is never cropped from the 2160×2700 (4:5) slide
render — that crop discards roughly 40% of the frame and cuts through
type. Any module used for Reels needs a vertical layout mode.

## Structure

- 15–18 seconds
- Five beats, roughly 3 seconds each
- **Frame 1 carries the complete hook** — legible in the first 0.5s,
  no build-up, no title card
- **Final frame closes the loop** back to frame 1 so the replay reads
  as continuous
- Silent-legible throughout: assume sound off, always

## Audio

Left empty at export. Trending audio is selected and attached at upload
— it cannot be chosen days in advance and stay current.

## Toolchain

`ffmpeg` is available in the build environment. Assembly is PNG
sequence → H.264 MP4, constant frame rate, no transitions beyond hard
cuts. Motion, if any, is a slow scale on a still — not animation.

## Source formats

FFFA and Split Decision cut best: both are already beat-structured.
Field Guide cuts poorly — 12 slides of dense argument does not compress
to 18 seconds without becoming a slideshow of headlines.
