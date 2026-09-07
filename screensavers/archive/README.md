# Helsing Archive

Eight public-domain works selected for Helsing’s scholarly atmosphere. These are unmodified museum images with their original colours and complete compositions.

## Collection and credits

All works are from The Metropolitan Museum of Art. The accompanying `sources/ID.json` records preserve each work’s `isPublicDomain: true` designation, artist, credit line and original image URL. The public-domain artworks are not relicensed under Helsing’s software licence.

| File | Work | Artist |
| --- | --- | --- |
| `10157.jpg` | [Study of Rocks and Trees by a Lake](https://www.metmuseum.org/art/collection/search/10157) | Albert Bierstadt |
| `13124.jpg` | [Interior View of the Metropolitan Museum of Art when in Fourteenth Street](https://www.metmuseum.org/art/collection/search/13124) | Frank Waller |
| `283066.jpg` | [A Scene in a Library](https://www.metmuseum.org/art/collection/search/283066) | William Henry Fox Talbot |
| `334749.jpg` | [Arch of Morning Glories](https://www.metmuseum.org/art/collection/search/334749) | Eugène Delacroix |
| `351722.jpg` | [Project for a Domed Building with Colonnaded Façade](https://www.metmuseum.org/art/collection/search/351722) | Anonymous, French, 18th century |
| `362554.jpg` | [Botanical Study](https://www.metmuseum.org/art/collection/search/362554) | Anonymous, French, 19th century |
| `364025.jpg` | [Study of trees](https://www.metmuseum.org/art/collection/search/364025) | Thomas Rowlandson |
| `435991.jpg` | [A Woman Reading](https://www.metmuseum.org/art/collection/search/435991) | Camille Corot |

## Installation

Download `images` and select it in your slideshow software. Use a 90-second interval, simple cuts and proportional fitting against `#F4F1EA`. Complete artworks are preserved on laptop and ultrawide screens; portrait works intentionally have parchment beside them.

For a single-screen mpv preview, run from this directory:

```bash
mpv --no-config --fullscreen --image-display-duration=90 --loop-playlist=inf --stop-screensaver=no --background=color --background-color='#F4F1EA' images/*.jpg
```

Press Escape to exit. This is not a screen lock. Desktop-specific idle detection belongs in your system configuration.

## cortadOS integration

The NixOS configuration vendors the collection for offline recovery. The existing five-minute idle timer selects it when the live theme is Helsing. Each active monitor gets an mpv viewer with the same shuffled order, one-second parchment fades and 30-second intervals. A gentle Ken Burns effect alternates zoom direction between slides, with 4–16% extra zoom, aspect-aware bounded panning and 120 updates per second. Portrait works travel vertically, wide works horizontally, and near-screen-shaped works move diagonally. Images fill the screen proportionally; portrait works are cropped more heavily on ultrawide displays. This uses more rendering resources than the static preview above, and does not modify the source files.

Activity dismisses all viewers. Escape and mouse movement also dismiss manual previews. New monitors are picked up on the next launch. Other themes retain their terminal savers. The original static version held each image for 90 seconds, which could appear not to advance during a short preview. The fade is rendered as a parchment OSD overlay from the same monotonic clock as Ken Burns, with redraws limited to transitions, preserving correct mpv still-image playlist timing.

Preview with `cortados-archive`, accelerate with `cortados-archive --interval 5`, or list installed files with `cortados-archive --check`. It does not change session locking, suspend or display-power policy.
