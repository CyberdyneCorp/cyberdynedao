"""Academy seed content - GeoAI: Deep Learning for Geospatial.

Deep learning applied to Earth observation: convolutional networks and
vision transformers for satellite and aerial imagery, semantic
segmentation and object detection, change detection, and the new wave of
geospatial foundation models (SatMAE, Prithvi). Every lesson is a direct
explanation with a mermaid diagram and a concrete PyTorch snippet or
formula, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz. It sits at the advanced end of the geospatial
track, connecting remote sensing with modern machine learning practice.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_GEOAI_DEEP_LEARNING = SeedCourse(
    slug="geoai-deep-learning",
    title="GeoAI: Deep Learning for Geospatial",
    description=(
        "Deep learning applied to Earth observation: CNNs and vision "
        "transformers for satellite and aerial imagery, semantic "
        "segmentation, object detection, change detection, and geospatial "
        "foundation models (SatMAE, Prithvi) - with real PyTorch snippets, "
        "spectral-index formulas and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# GeoAI: Deep Learning for Geospatial

Earth observation now produces more imagery than humans can ever look at:
Sentinel-2 alone images the whole planet every few days at 10 m
resolution. **GeoAI** is the practice of turning that flood of pixels into
maps, counts, and change alerts using deep learning. This course connects
what you know about remote sensing (bands, projections, GeoTIFFs) with
modern neural networks (CNNs and transformers).

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short **PyTorch** snippet or a formula, and draws the
pipeline as a diagram. After each lesson there is a short quiz; at the
end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **From pixels to labels** - why deep learning suits imagery
2. **Preparing training data** - tiles, labels, and augmentation
3. **CNNs for scene classification** - one label per image
4. **Semantic segmentation** - a label for every pixel (U-Net)
5. **Object detection** - boxes around ships, planes, buildings
6. **Change detection** - what is different between two dates
7. **Vision transformers and foundation models** - SatMAE, Prithvi
8. **MLOps for geospatial** - inference at scale and honest evaluation

This is the map. You should already be comfortable with raster data,
coordinate reference systems (EPSG:4326 vs a projected UTM CRS), and the
Sentinel and Landsat missions - this course adds the learning on top.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is GeoAI, as used in this course?",
                    (
                        opt("A single satellite operated by one agency"),
                        opt("A file format for storing coordinates"),
                        opt(
                            "The practice of applying deep learning to Earth "
                            "observation imagery to produce maps, counts and change "
                            "detection",
                            correct=True,
                        ),
                        opt("A replacement for coordinate reference systems"),
                    ),
                    "GeoAI turns the flood of satellite and aerial pixels into "
                    "labels, masks and change maps using neural networks.",
                ),
                q(
                    "Why is deep learning attractive for Earth observation right now?",
                    (
                        opt("Because satellites stopped producing data"),
                        opt(
                            "Missions like Sentinel-2 image the planet every few days, "
                            "producing far more imagery than people can inspect by hand",
                            correct=True,
                        ),
                        opt("Because pixels no longer have coordinates"),
                        opt("Because CRS transforms became impossible"),
                    ),
                    "The data volume is the driver: automation is the only way to "
                    "keep up with continuous global coverage.",
                ),
            ),
        ),
        # -- 1. From pixels to labels ----------------------------------
        _t(
            "From pixels to labels: deep learning for imagery",
            "10 min",
            """# From pixels to labels: deep learning for imagery

A satellite image is a **tensor**: height by width by channels. A
Sentinel-2 tile might be `[13, 512, 512]` - 13 spectral bands, each a
512 by 512 grid of reflectance values. Classic remote sensing hand-crafts
features from these bands (for example the **NDVI** vegetation index):

```text
NDVI = (NIR - Red) / (NIR + Red)
```

That works, but a human has to design each feature. **Deep learning**
instead *learns* the features. A **convolutional neural network (CNN)**
slides small learnable filters across the image; early layers learn edges
and textures, deeper layers learn crops, roads, rooftops - all fitted from
labelled examples rather than written by hand.

Earth observation imagery differs from ordinary photos in ways that
matter:

- **More than 3 channels** - not just RGB. Red-edge, near-infrared and
  short-wave infrared carry vegetation, water and moisture signal, so a
  model input layer must accept `in_channels` beyond 3.
- **Physical scale** - every pixel covers a known ground distance (10 m
  for Sentinel-2 visible bands). Object size in pixels is meaningful.
- **Georeferenced** - each pixel maps to a coordinate through the raster's
  CRS and geotransform, so predictions become real map layers.

The task you choose defines the output shape:

```mermaid
graph LR
    IMG["Image tensor bands by H by W"] --> MODEL["Neural network"]
    MODEL --> CLS["Classification one label per tile"]
    MODEL --> SEG["Segmentation one label per pixel"]
    MODEL --> DET["Detection boxes with classes"]
    MODEL --> CHG["Change detection difference map"]
```

A minimal first layer that accepts all 13 Sentinel-2 bands:

```python
import torch.nn as nn

# a conv that reads 13 spectral bands, not just RGB
first = nn.Conv2d(in_channels=13, out_channels=64, kernel_size=3, padding=1)
```

Remember: deep learning replaces hand-designed indices with features
learned from labelled imagery - but the geospatial context (extra bands,
ground scale, georeferencing) stays essential.
""",
        ),
        quiz_lesson(
            "Quiz: From pixels to labels: deep learning for imagery",
            (
                q(
                    "How is a multispectral satellite tile represented for a neural network?",
                    (
                        opt("As a single scalar number"),
                        opt(
                            "As a tensor of channels by height by width, where channels "
                            "are the spectral bands",
                            correct=True,
                        ),
                        opt("As a list of latitude and longitude pairs only"),
                        opt("As plain text describing the scene"),
                    ),
                    "A Sentinel-2 tile is bands by H by W - for example 13 by 512 by "
                    "512; the bands are the input channels.",
                ),
                q(
                    "What is the key difference between classic indices like NDVI and a CNN?",
                    (
                        opt("NDVI needs a GPU; CNNs do not"),
                        opt(
                            "NDVI is a hand-designed feature; a CNN learns its features "
                            "from labelled examples",
                            correct=True,
                        ),
                        opt("CNNs cannot read infrared bands"),
                        opt("They are identical operations"),
                    ),
                    "NDVI = (NIR - Red) / (NIR + Red) is written by a human; a CNN "
                    "fits its filters to the data.",
                ),
                q(
                    "Why must a geospatial model input often accept more than 3 channels?",
                    (
                        opt("To store the file name"),
                        opt("Because RGB is illegal in remote sensing"),
                        opt(
                            "Because near-infrared and short-wave infrared bands carry "
                            "vegetation, water and moisture signal beyond RGB",
                            correct=True,
                        ),
                        opt("To make the tensor square"),
                    ),
                    "Set in_channels to the number of bands you feed; the extra bands "
                    "carry information RGB alone lacks.",
                ),
            ),
        ),
        # -- 2. Preparing training data --------------------------------
        _t(
            "Preparing geospatial training data (tiles, labels, augmentation)",
            "11 min",
            """# Preparing geospatial training data (tiles, labels, augmentation)

Models are only as good as their data, and geospatial data needs care
before it can train anything. A full Sentinel-2 scene is far too large for
a GPU, so you **tile** it into fixed patches (say 256 by 256) with a
little overlap, keeping each tile's geotransform so predictions can be
stitched back into a georeferenced map.

The labels must line up with the pixels. For **segmentation** you
rasterize vector polygons (land-cover classes) onto the same grid as the
imagery, in the same CRS:

```python
import rasterio
from rasterio.features import rasterize

with rasterio.open("scene.tif") as src:
    # burn class polygons onto the image grid to make a label mask
    mask = rasterize(
        ((geom, class_id) for geom, class_id in shapes),
        out_shape=(src.height, src.width),
        transform=src.transform,   # SAME grid as the imagery
    )
```

Three rules keep the dataset honest:

- **Normalize per band** - reflectance ranges differ across bands.
  Subtract each band's mean and divide by its standard deviation so no
  band dominates: `x = (x - mean) / std`.
- **Split by geography, not at random** - random tile splits leak, because
  neighbouring tiles are nearly identical. Split by **region or scene** so
  the validation area is genuinely unseen.
- **Handle class imbalance** - rare classes (landslides, solar farms) need
  weighting or oversampling, or the model just predicts "background".

**Augmentation** multiplies your labelled data by transforming tiles.
Geometric flips and 90-degree rotations are safe because imagery is
roughly rotation-invariant from above; be careful with colour jitter so
you do not destroy the physical meaning of the bands.

```mermaid
graph TD
    SCENE["Full georeferenced scene"] --> TILE["Tile into fixed patches"]
    VECTOR["Label polygons in same CRS"] --> RAST["Rasterize to mask"]
    TILE --> NORM["Normalize per band"]
    RAST --> NORM
    NORM --> SPLIT["Split by region not random"]
    SPLIT --> AUG["Augment flips and rotations"]
    AUG --> READY["Training ready dataset"]
```

Remember: align labels to the imagery grid and CRS, normalize per band,
split by geography to avoid leakage, and augment with transforms that
respect the physics of the bands.
""",
        ),
        quiz_lesson(
            "Quiz: Preparing geospatial training data (tiles, labels, augmentation)",
            (
                q(
                    "Why split a geospatial dataset by region rather than by random tiles?",
                    (
                        opt("Random splits are slower to compute"),
                        opt(
                            "Neighbouring tiles are nearly identical, so a random split "
                            "leaks information and inflates validation scores",
                            correct=True,
                        ),
                        opt("Regions have prettier boundaries"),
                        opt("Random splitting corrupts the GeoTIFF"),
                    ),
                    "Spatial autocorrelation means adjacent tiles look alike; split "
                    "by scene or region so validation is truly unseen.",
                ),
                q(
                    "When rasterizing label polygons for segmentation, what must match the imagery?",
                    (
                        opt("The file name only"),
                        opt("The compression codec"),
                        opt(
                            "The grid (shape and transform) and the CRS, so labels "
                            "align pixel-for-pixel with the image",
                            correct=True,
                        ),
                        opt("The satellite's orbit number"),
                    ),
                    "Burn polygons onto the same out_shape and transform as the "
                    "raster so each mask pixel matches its image pixel.",
                ),
                q(
                    "Which augmentation is generally safe for overhead imagery?",
                    (
                        opt("Nothing can be augmented"),
                        opt(
                            "Geometric flips and 90-degree rotations, because overhead "
                            "imagery is roughly rotation-invariant",
                            correct=True,
                        ),
                        opt("Deleting random bands every batch"),
                        opt("Rewriting the coordinates randomly"),
                    ),
                    "Flips and right-angle rotations respect the top-down geometry; "
                    "aggressive colour changes can destroy band physics.",
                ),
            ),
        ),
        # -- 3. CNNs for scene classification --------------------------
        _t(
            "CNNs for scene classification",
            "10 min",
            """# CNNs for scene classification

**Scene classification** assigns **one label to a whole tile**: this patch
is "forest", "residential", "water", or "cropland". It is the simplest
GeoAI task and a good place to understand how a **CNN** turns pixels into
a decision.

A CNN stacks three ideas:

- **Convolution** - slide a small learnable filter over the image; it
  responds to a local pattern (an edge, a texture) wherever it appears.
  Sharing the filter across the image is what makes it efficient and
  translation-tolerant.
- **Pooling / stride** - downsample so deeper layers see a larger area
  (the **receptive field** grows) while the map shrinks.
- **Nonlinearity** - a ReLU after each convolution lets the network learn
  patterns that are not just linear mixes of bands.

The output of a convolution at one location is a weighted sum over a
window plus a bias, then a nonlinearity:

```text
out(i,j) = ReLU( sum over window of  W * input  +  b )
```

Rather than train from scratch, you almost always start from a
**pretrained backbone** (ResNet, EfficientNet) and **fine-tune** it. The
one twist for geospatial: adapt the first layer to your band count, and if
you have few labels, use **transfer learning** so the network reuses
generic edge and texture filters:

```python
import torch.nn as nn
from torchvision.models import resnet18

model = resnet18(weights="IMAGENET1K_V1")
# adapt the stem to 13 Sentinel-2 bands instead of 3 (RGB)
model.conv1 = nn.Conv2d(13, 64, kernel_size=7, stride=2, padding=3, bias=False)
# swap the head for our number of land-cover classes
model.fc = nn.Linear(model.fc.in_features, 10)
```

```mermaid
graph LR
    TILE["Input tile bands by H by W"] --> C1["Conv and ReLU edges"]
    C1 --> P1["Pool downsample"]
    P1 --> C2["Conv and ReLU textures"]
    C2 --> P2["Pool downsample"]
    P2 --> GAP["Global average pool"]
    GAP --> FC["Fully connected head"]
    FC --> LABEL["One class per tile"]
```

Datasets like **EuroSAT** (Sentinel-2 land-use patches) and **UC Merced**
are the classic benchmarks here. Remember: classification gives one label
per tile; a pretrained backbone with an adapted stem and head gets you
strong results from modest labelled data.
""",
        ),
        quiz_lesson(
            "Quiz: CNNs for scene classification",
            (
                q(
                    "What does scene classification output for an input tile?",
                    (
                        opt("A label for every pixel"),
                        opt("Bounding boxes around objects"),
                        opt("One class label for the whole tile", correct=True),
                        opt("A change map between two dates"),
                    ),
                    "Classification is one label per image (for example EuroSAT "
                    "land-use classes); per-pixel labels are segmentation.",
                ),
                q(
                    "Why does pooling or striding help a CNN?",
                    (
                        opt("It adds more color to the image"),
                        opt(
                            "It downsamples so deeper layers have a larger receptive "
                            "field and see broader context",
                            correct=True,
                        ),
                        opt("It stores the coordinate reference system"),
                        opt("It removes the need for labels"),
                    ),
                    "Downsampling grows the receptive field: deeper filters respond "
                    "to larger structures.",
                ),
                q(
                    "When fine-tuning a pretrained ImageNet backbone on 13-band imagery, what changes?",
                    (
                        opt("Nothing; it works unmodified"),
                        opt(
                            "Adapt the first conv layer to accept the band count and "
                            "replace the classifier head with your number of classes",
                            correct=True,
                        ),
                        opt("You must retrain ImageNet from scratch"),
                        opt("You delete all convolution layers"),
                    ),
                    "The RGB stem cannot read 13 bands, and the head must match your "
                    "class count; the middle layers transfer usefully.",
                ),
            ),
        ),
        # -- 4. Semantic segmentation (U-Net) --------------------------
        _t(
            "Semantic segmentation (U-Net) for land cover",
            "11 min",
            """# Semantic segmentation (U-Net) for land cover

**Semantic segmentation** assigns a class to **every pixel**, producing a
dense **land-cover map**: this pixel is water, that one is built-up, the
next is forest. Where classification asks "what is in this tile?",
segmentation asks "what is at every location?" - exactly what mapping
needs.

The dominant architecture is the **U-Net**, an **encoder-decoder** with
**skip connections**:

- The **encoder** (contracting path) downsamples, capturing *what* is
  present with a growing receptive field - like a classifier.
- The **decoder** (expanding path) upsamples back to full resolution,
  recovering *where* things are.
- **Skip connections** copy high-resolution features from the encoder
  straight across to the decoder, so sharp boundaries (a coastline, a
  field edge) are not lost during downsampling. The "U" shape comes from
  drawing the encoder down one side and the decoder up the other.

The output is a class score per pixel; you train with per-pixel
cross-entropy, often plus a **Dice loss** that directly rewards overlap
with the true mask - helpful for thin or rare classes:

```text
Dice = (2 * |Prediction intersect Truth|) / (|Prediction| + |Truth|)
```

```python
import segmentation_models_pytorch as smp

# U-Net with a pretrained encoder, 13 input bands, 6 land-cover classes
model = smp.Unet(
    encoder_name="resnet34",
    in_channels=13,
    classes=6,
)
# logits shape: [batch, 6, H, W] -> argmax over classes gives the map
```

```mermaid
graph LR
    IN["Image tile"] --> E1["Encoder downsample"]
    E1 --> E2["Encoder downsample more"]
    E2 --> B["Bottleneck what is present"]
    B --> D2["Decoder upsample"]
    D2 --> D1["Decoder upsample to full res"]
    D1 --> OUT["Per pixel class map"]
    E1 -->|"skip"| D1
    E2 -->|"skip"| D2
```

Evaluate segmentation with **IoU** (intersection over union) per class and
its mean (**mIoU**), not plain accuracy - accuracy is misleading when one
class dominates the scene. Remember: the encoder finds what, the decoder
and skips restore where, and mIoU tells you how good the map really is.
""",
        ),
        quiz_lesson(
            "Quiz: Semantic segmentation (U-Net) for land cover",
            (
                q(
                    "What does semantic segmentation produce?",
                    (
                        opt("One label for the whole tile"),
                        opt("A class label for every pixel", correct=True),
                        opt("A single bounding box"),
                        opt("Only the image histogram"),
                    ),
                    "Segmentation is dense prediction - a land-cover class at every "
                    "pixel, ideal for mapping.",
                ),
                q(
                    "What do the skip connections in a U-Net do?",
                    (
                        opt("They skip training to save time"),
                        opt(
                            "They carry high-resolution encoder features to the "
                            "decoder so sharp boundaries are preserved",
                            correct=True,
                        ),
                        opt("They delete the bottleneck"),
                        opt("They convert the CRS"),
                    ),
                    "Downsampling loses spatial detail; skips restore it so edges "
                    "like coastlines stay crisp.",
                ),
                q(
                    "Why prefer mean IoU over plain accuracy for land-cover segmentation?",
                    (
                        opt("IoU is easier to spell"),
                        opt(
                            "Accuracy is misleading when one class dominates; IoU per "
                            "class measures overlap fairly, including rare classes",
                            correct=True,
                        ),
                        opt("Accuracy cannot be computed on rasters"),
                        opt("IoU ignores the labels entirely"),
                    ),
                    "If 90 percent of pixels are one class, predicting only that "
                    "class scores high accuracy but poor mIoU.",
                ),
            ),
        ),
        # -- 5. Object detection ---------------------------------------
        _t(
            "Object detection in aerial and satellite imagery",
            "11 min",
            """# Object detection in aerial and satellite imagery

**Object detection** finds and **localizes discrete things** - each ship,
aircraft, storage tank, or vehicle gets a **bounding box** plus a class
and a confidence. It answers "where are the objects and how many?", which
segmentation (regions) and classification (one label) do not.

Overhead detection has its own character:

- **Objects are small** - a car may be 10 by 20 pixels; a model must keep
  fine spatial detail, so input tiles are often larger and higher
  resolution.
- **Any orientation** - a ship can point any way. Standard axis-aligned
  boxes fit loosely, so aerial work often uses **oriented (rotated)
  bounding boxes**.
- **Dense and clustered** - parking lots, container yards - many objects
  packed together stress the box-suppression step.

Modern detectors (the **YOLO** family, Faster R-CNN, DETR) predict many
candidate boxes, then remove duplicates with **non-maximum suppression
(NMS)** using the box overlap (**IoU**) between candidates:

```text
IoU(A,B) = area(A intersect B) / area(A union B)
# NMS keeps the highest-confidence box, drops others with IoU above a threshold
```

```python
import torch
from torchvision.ops import nms

# boxes [N,4] xyxy, scores [N]; drop overlapping duplicates
keep = nms(boxes, scores, iou_threshold=0.5)
final_boxes = boxes[keep]
```

```mermaid
graph LR
    TILE["Large high res tile"] --> BACK["Backbone features"]
    BACK --> HEAD["Detection head many boxes"]
    HEAD --> SCORE["Boxes with class and score"]
    SCORE --> NMS["Non maximum suppression"]
    NMS --> OUT["Final boxes counted and mapped"]
```

Because objects have a known ground size (each pixel is a fixed distance),
you can filter physically impossible detections and convert box centers
into real coordinates through the raster geotransform - turning boxes into
a point layer of ships or aircraft. Benchmarks like **DOTA** and **xView**
drive this work. Remember: detection gives per-object boxes; small,
rotated, clustered targets and NMS by IoU are the defining challenges.
""",
        ),
        quiz_lesson(
            "Quiz: Object detection in aerial and satellite imagery",
            (
                q(
                    "What does object detection output that classification does not?",
                    (
                        opt("A single global label"),
                        opt(
                            "A bounding box, class and confidence for each individual "
                            "object, so objects can be located and counted",
                            correct=True,
                        ),
                        opt("Only a per-pixel mask"),
                        opt("The CRS of the scene"),
                    ),
                    "Detection localizes and counts discrete objects; classification "
                    "gives one label for the whole tile.",
                ),
                q(
                    "What is non-maximum suppression (NMS) used for?",
                    (
                        opt("Increasing image brightness"),
                        opt(
                            "Removing duplicate overlapping boxes, keeping the highest "
                            "confidence one based on IoU overlap",
                            correct=True,
                        ),
                        opt("Rasterizing polygons"),
                        opt("Splitting the dataset by region"),
                    ),
                    "Detectors emit many overlapping candidates; NMS keeps the best "
                    "per object using an IoU threshold.",
                ),
                q(
                    "Why are oriented bounding boxes common in aerial detection?",
                    (
                        opt("They render faster"),
                        opt(
                            "Overhead objects such as ships appear at any orientation, "
                            "which axis-aligned boxes fit loosely",
                            correct=True,
                        ),
                        opt("They avoid needing any training data"),
                        opt("They are required by GeoTIFF"),
                    ),
                    "A rotated box hugs an angled ship tightly where an axis-aligned "
                    "box would include much background.",
                ),
            ),
        ),
        # -- 6. Change detection ---------------------------------------
        _t(
            "Change detection with deep learning",
            "11 min",
            """# Change detection with deep learning

**Change detection** compares imagery of the **same place at two (or more)
dates** and maps what is different - new buildings, deforestation, flood
extent, a burn scar. It is one of the highest-value Earth-observation
tasks because it turns repeat coverage into alerts.

The hard part is separating **real change** from **nuisance change**:
different sun angle, season, clouds, or a slight misregistration between
dates all shift pixels without anything actually changing on the ground.
So two things come first:

- **Co-register** the images so a pixel at date 1 and date 2 is the same
  ground location (sub-pixel alignment matters).
- **Normalize** illumination and atmosphere so brightness differences are
  not read as change.

The deep-learning approach is usually a **Siamese network**: the *same*
encoder (shared weights) embeds each date, and the decoder learns to map
the *difference* of the two embeddings to a change mask - far more robust
than a raw pixel subtraction:

```python
class SiameseChange(nn.Module):
    def forward(self, img_t1, img_t2):
        f1 = self.encoder(img_t1)      # shared weights
        f2 = self.encoder(img_t2)      # same encoder
        diff = torch.abs(f1 - f2)      # compare in feature space
        return self.decoder(diff)      # -> change probability per pixel
```

A quick pixel baseline is differencing an index between dates, for example
burned area via the normalized burn ratio:

```text
dNBR = NBR_before - NBR_after      # higher dNBR means more severe burn
```

```mermaid
graph LR
    T1["Image date 1"] --> REG["Co register and normalize"]
    T2["Image date 2"] --> REG
    REG --> ENC["Shared encoder both dates"]
    ENC --> DIFF["Compare in feature space"]
    DIFF --> DEC["Decoder"]
    DEC --> MAP["Change mask what differs"]
```

Evaluate with F1 or IoU on the change class, and watch for the imbalance:
most of a scene usually does **not** change, so a model can score high by
predicting "no change" everywhere - weight the loss accordingly. Remember:
align and normalize first, compare in learned feature space with shared
weights, and treat change as the rare, valuable class.
""",
        ),
        quiz_lesson(
            "Quiz: Change detection with deep learning",
            (
                q(
                    "What is the goal of change detection?",
                    (
                        opt("Classify a single image into one land-use class"),
                        opt(
                            "Compare imagery of the same place at different dates and "
                            "map what actually changed on the ground",
                            correct=True,
                        ),
                        opt("Draw boxes around every vehicle"),
                        opt("Convert a raster to a new CRS"),
                    ),
                    "Change detection exploits repeat coverage to flag differences "
                    "such as new buildings, floods or deforestation.",
                ),
                q(
                    "Why co-register and normalize the two dates before detecting change?",
                    (
                        opt("To make the files smaller"),
                        opt(
                            "So a pixel means the same ground location and brightness "
                            "differences from sun or season are not mistaken for change",
                            correct=True,
                        ),
                        opt("Because change detection needs no labels"),
                        opt("To remove the near-infrared band"),
                    ),
                    "Misregistration and illumination differences are nuisance change; "
                    "aligning and normalizing removes them first.",
                ),
                q(
                    "What is a Siamese network in this context?",
                    (
                        opt("Two unrelated models trained separately"),
                        opt(
                            "One shared-weight encoder that embeds both dates so they "
                            "can be compared in feature space",
                            correct=True,
                        ),
                        opt("A network that only reads RGB"),
                        opt("A tool that georeferences rasters"),
                    ),
                    "Shared weights ensure both dates are embedded the same way; the "
                    "model learns the difference, not raw pixel subtraction.",
                ),
            ),
        ),
        # -- 7. ViTs and foundation models -----------------------------
        _t(
            "Vision transformers and geospatial foundation models (SatMAE, Prithvi)",
            "12 min",
            """# Vision transformers and geospatial foundation models

CNNs read images through small local filters. A **vision transformer
(ViT)** takes a different route: it cuts the image into a grid of
**patches**, embeds each patch as a token, and uses **self-attention** so
every patch can relate to every other patch directly. That global view
suits large scenes where context far apart matters (a river system, an
urban footprint).

Attention weighs how much each token should attend to the others:

```text
Attention(Q, K, V) = softmax( Q * K^T / sqrt(d) ) * V
```

The bigger shift is the **foundation model** idea. Labels are scarce in
Earth observation, but *unlabelled* imagery is nearly infinite. So you
**pretrain** a large model on huge unlabelled archives with a
**self-supervised** objective, then **fine-tune** it on your small
labelled task. Two geospatial examples:

- **SatMAE** - a **masked autoencoder** for satellite imagery: hide most
  of the image patches and train the model to reconstruct them, so it
  learns structure without any labels. It also handles multispectral bands
  and temporal sequences.
- **Prithvi** - a geospatial foundation model (IBM and NASA) pretrained on
  large volumes of Harmonized Landsat-Sentinel data, released for
  fine-tuning on tasks like flood mapping, burn scars and crop
  segmentation.

```python
# use a pretrained geospatial backbone, then fine-tune a small head
backbone = load_pretrained("prithvi")     # self-supervised on HLS imagery
for p in backbone.parameters():
    p.requires_grad = False               # freeze; train just the head
head = nn.Conv2d(backbone.embed_dim, num_classes, kernel_size=1)
```

```mermaid
graph TD
    ARCH["Huge unlabelled archive"] --> PRE["Self supervised pretrain"]
    PRE --> FM["Foundation model weights"]
    FM --> FT1["Fine tune flood mapping"]
    FM --> FT2["Fine tune crop segmentation"]
    FM --> FT3["Fine tune burn scars"]
```

The payoff: instead of training each task from scratch on scarce labels,
you adapt a model that already understands imagery, reaching good accuracy
with far fewer labels. Remember: ViTs bring global attention over patches,
and geospatial foundation models (SatMAE, Prithvi) pretrain on unlabelled
archives so downstream tasks need only light fine-tuning.
""",
        ),
        quiz_lesson(
            "Quiz: Vision transformers and geospatial foundation models (SatMAE, Prithvi)",
            (
                q(
                    "How does a vision transformer process an image?",
                    (
                        opt("It only reads the center pixel"),
                        opt(
                            "It splits the image into patches, embeds each as a token, "
                            "and uses self-attention so patches relate globally",
                            correct=True,
                        ),
                        opt("It converts the image to a single number first"),
                        opt("It requires exactly three bands"),
                    ),
                    "Patches become tokens; self-attention lets distant regions "
                    "interact directly, giving a global view.",
                ),
                q(
                    "What is the core idea of a geospatial foundation model like SatMAE or Prithvi?",
                    (
                        opt("Train separately from scratch on every task"),
                        opt(
                            "Pretrain on huge unlabelled imagery with a self-supervised "
                            "objective, then fine-tune on small labelled tasks",
                            correct=True,
                        ),
                        opt("Avoid using satellite imagery entirely"),
                        opt("Only work on RGB photos"),
                    ),
                    "Unlabelled imagery is abundant; self-supervised pretraining "
                    "yields weights that fine-tune well with few labels.",
                ),
                q(
                    "What self-supervised task does a masked autoencoder like SatMAE use?",
                    (
                        opt("Predicting the file name"),
                        opt(
                            "Hiding most image patches and training the model to "
                            "reconstruct them, learning structure without labels",
                            correct=True,
                        ),
                        opt("Manually labelling every pixel"),
                        opt("Sorting tiles by acquisition date"),
                    ),
                    "Mask-and-reconstruct forces the model to learn image structure "
                    "with no human labels at all.",
                ),
            ),
        ),
        # -- 8. MLOps for geospatial -----------------------------------
        _t(
            "MLOps for geospatial: inference at scale and evaluation",
            "11 min",
            """# MLOps for geospatial: inference at scale and evaluation

A trained model is worthless until it runs reliably on real scenes and you
can trust its numbers. **Geospatial MLOps** is inference at scale plus
honest evaluation plus keeping the model healthy over time.

**Inference at scale.** Scenes are gigapixels, so you run the model in the
same tiles you trained on - but the seams show. Two techniques matter:

- **Overlapping tiles** - predict on patches that overlap, then blend, so
  objects split across a tile edge are not cut in half.
- **Georeferenced stitching** - write predictions back with each tile's
  transform and CRS so the mosaic is a valid map layer (a GeoTIFF or, for
  segmentation, vectorized polygons).

```python
with rasterio.open("out.tif", "w", **profile) as dst:
    for tile, window in tiled(scene, size=512, overlap=64):
        pred = model(preprocess(tile)).argmax(1)   # class per pixel
        dst.write(pred.numpy(), window=window)     # georeferenced write
```

**Honest evaluation.** Report the metric that matches the task and never
on data seen in training:

- Classification: precision, recall, F1 (accuracy alone hides imbalance).
- Segmentation: mean IoU per class.
- Detection: mean average precision (**mAP**) at an IoU threshold.
- Always keep a **spatially held-out** test region - a different scene or
  area - so the score reflects new geography, not memorized tiles.

**Keep it healthy.** Sensors, seasons and land use drift, so a model
degrades over time (**domain shift**). Monitor prediction distributions,
sample outputs for review, and plan to retrain - and record model version,
training data, and CRS assumptions for reproducibility.

```mermaid
graph LR
    SCENE["New scene gigapixels"] --> TILES["Overlapping tiles"]
    TILES --> INFER["Model inference"]
    INFER --> STITCH["Georeferenced stitch"]
    STITCH --> MAP["Map layer GeoTIFF or vectors"]
    MAP --> EVAL["Evaluate on held out region"]
    EVAL --> MON["Monitor drift and retrain"]
    MON --> INFER
```

Remember: predict on overlapping tiles and stitch back into a real map,
evaluate with task-appropriate metrics on spatially held-out data, and
monitor for drift so the model stays trustworthy in production.
""",
        ),
        quiz_lesson(
            "Quiz: MLOps for geospatial: inference at scale and evaluation",
            (
                q(
                    "Why run inference on overlapping tiles for a large scene?",
                    (
                        opt("To make the output file larger on purpose"),
                        opt(
                            "So objects split across tile edges are not cut in half; "
                            "overlapping predictions are blended at the seams",
                            correct=True,
                        ),
                        opt("Because non-overlapping tiles are illegal"),
                        opt("To change the coordinate reference system"),
                    ),
                    "Edge artifacts appear at tile boundaries; overlap and blend "
                    "removes the seams in the mosaic.",
                ),
                q(
                    "What is the right evaluation discipline for a geospatial model?",
                    (
                        opt("Test on the same tiles used in training"),
                        opt(
                            "Use task-appropriate metrics on a spatially held-out "
                            "region so the score reflects new geography",
                            correct=True,
                        ),
                        opt("Report only training accuracy"),
                        opt("Never compute any metric"),
                    ),
                    "Hold out a different scene or area; adjacent tiles leak, so "
                    "same-area testing overstates real performance.",
                ),
                q(
                    "What is domain shift and why does it matter in production?",
                    (
                        opt("A change in file format"),
                        opt(
                            "Sensors, seasons and land use drift over time, so a model "
                            "degrades and must be monitored and retrained",
                            correct=True,
                        ),
                        opt("A bug in the GeoTIFF header"),
                        opt("A type of coordinate transform"),
                    ),
                    "The world the model sees changes; monitoring predictions and "
                    "retraining keeps it trustworthy.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "How is a multispectral tile fed to a neural network, and what does a CNN learn?",
                    (
                        opt("As text; the CNN learns to spell class names"),
                        opt(
                            "As a channels-by-H-by-W tensor; the CNN learns features "
                            "from labelled data instead of hand-designed indices",
                            correct=True,
                        ),
                        opt("As a list of coordinates; the CNN learns projections"),
                        opt("As a single scalar; the CNN learns nothing"),
                    ),
                    "Bands are input channels; convolution learns edges and textures "
                    "that classic indices like NDVI encode by hand.",
                ),
                q(
                    "Why split geospatial data by region rather than randomly?",
                    (
                        opt("Random splits are illegal"),
                        opt(
                            "Neighbouring tiles are nearly identical, so random splits "
                            "leak and inflate validation scores",
                            correct=True,
                        ),
                        opt("Regions compress better"),
                        opt("It changes the CRS"),
                    ),
                    "Spatial autocorrelation means adjacent tiles are alike; split "
                    "by scene so validation is genuinely unseen.",
                ),
                q(
                    "Classification, segmentation and detection differ in output. Which mapping is correct?",
                    (
                        opt("Classification gives per-pixel masks"),
                        opt(
                            "Classification gives one label per tile, segmentation a "
                            "label per pixel, detection a box per object",
                            correct=True,
                        ),
                        opt("Detection gives one label per tile"),
                        opt("Segmentation gives one box per object"),
                    ),
                    "One label per tile, per-pixel labels, and per-object boxes are "
                    "the three output shapes.",
                ),
                q(
                    "What role do skip connections play in a U-Net?",
                    (
                        opt("They skip training epochs"),
                        opt(
                            "They pass high-resolution encoder features to the decoder "
                            "so boundaries stay sharp",
                            correct=True,
                        ),
                        opt("They remove the bottleneck layer"),
                        opt("They store the geotransform"),
                    ),
                    "Encoder learns what, decoder plus skips restore where, keeping "
                    "edges crisp after downsampling.",
                ),
                q(
                    "In object detection, what does non-maximum suppression do?",
                    (
                        opt("Brightens the image"),
                        opt(
                            "Removes duplicate overlapping boxes using IoU, keeping the "
                            "highest-confidence detection per object",
                            correct=True,
                        ),
                        opt("Rasterizes label polygons"),
                        opt("Normalizes the bands"),
                    ),
                    "Detectors emit many candidates; NMS deduplicates by IoU overlap.",
                ),
                q(
                    "Why is a Siamese, shared-weight encoder used for change detection?",
                    (
                        opt("To read only RGB bands"),
                        opt(
                            "So both dates are embedded the same way and the model "
                            "compares them in feature space, not raw pixels",
                            correct=True,
                        ),
                        opt("To avoid needing two dates"),
                        opt("To convert coordinates faster"),
                    ),
                    "Shared weights make the two embeddings comparable; learning the "
                    "difference beats raw pixel subtraction.",
                ),
                q(
                    "Before comparing two dates for change, what must you do first?",
                    (
                        opt("Delete the near-infrared band"),
                        opt(
                            "Co-register and normalize the images so alignment and "
                            "brightness differences are not read as change",
                            correct=True,
                        ),
                        opt("Randomly shuffle the pixels"),
                        opt("Convert both to JPEG"),
                    ),
                    "Misregistration and illumination are nuisance change; align and "
                    "normalize to isolate real change.",
                ),
                q(
                    "What is the core idea behind geospatial foundation models such as SatMAE and Prithvi?",
                    (
                        opt("Train from scratch on every new task"),
                        opt(
                            "Pretrain self-supervised on huge unlabelled imagery, then "
                            "fine-tune on small labelled tasks",
                            correct=True,
                        ),
                        opt("Only use hand-labelled data"),
                        opt("Avoid transformers entirely"),
                    ),
                    "Abundant unlabelled imagery pretrains a model that fine-tunes "
                    "well with few labels.",
                ),
                q(
                    "Which metric suits imbalanced land-cover segmentation better than plain accuracy?",
                    (
                        opt("File size"),
                        opt("Mean IoU per class", correct=True),
                        opt("Deployment frequency"),
                        opt("Pixel brightness"),
                    ),
                    "When one class dominates, accuracy is misleading; mean IoU "
                    "measures overlap fairly across classes.",
                ),
                q(
                    "Why must geospatial models be monitored after deployment?",
                    (
                        opt("GeoTIFF headers expire"),
                        opt(
                            "Sensors, seasons and land use drift over time (domain "
                            "shift), so accuracy degrades and retraining is needed",
                            correct=True,
                        ),
                        opt("Coordinates change every night"),
                        opt("Models never change once trained"),
                    ),
                    "The world the model sees shifts; monitoring and retraining keep "
                    "predictions trustworthy.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GEOAI_DEEP_LEARNING_COURSES: tuple[SeedCourse, ...] = (_GEOAI_DEEP_LEARNING,)
