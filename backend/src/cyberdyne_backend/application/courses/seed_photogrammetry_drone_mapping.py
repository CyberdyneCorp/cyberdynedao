"""Academy seed content - Photogrammetry and Drone Mapping.

Reconstructing 3D reality from photographs: the geometry of a camera (the
pinhole model), interior and exterior orientation, stereoscopy and the
collinearity equations, structure from motion and bundle adjustment,
ground control and georeferencing, dense matching to point clouds, digital
surface and terrain models, and the end-to-end drone mapping workflow that
produces orthomosaics, DSMs and DTMs. Every lesson is a direct explanation
with a concrete formula or code example and a mermaid diagram, followed by
a checkpoint quiz; the course closes with a comprehensive final quiz.
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


_PHOTOGRAMMETRY_DRONE_MAPPING = SeedCourse(
    slug="photogrammetry-drone-mapping",
    title="Photogrammetry & Drone Mapping",
    description=(
        "Reconstructing 3D reality from photographs - camera geometry, "
        "stereoscopy, structure from motion, and drone mapping workflows that "
        "produce orthomosaics, DSMs and DTMs. Every lesson pairs a direct "
        "explanation with a real formula or code example and a diagram, from "
        "the pinhole model through bundle adjustment to Pix4D and OpenDroneMap."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Photogrammetry and Drone Mapping

Photogrammetry is the science of **measuring the world from photographs**.
Point a camera at a scene from two or more positions and, if you know how
the camera behaves and where it was, you can recover the 3D coordinates of
everything it saw. Modern drones automate the capture; modern software
automates the maths. The result is survey-grade 3D: orthomosaics, digital
surface models, and terrain models.

The approach here is **direct and concrete**: every lesson explains one
idea, grounds it in a real formula or a short code snippet
(NumPy/OpenCV/GDAL), and draws it as a diagram. After each lesson there is
a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Camera geometry** - the pinhole model and the projection matrix
2. **Interior and exterior orientation** - calibration and camera pose
3. **Stereoscopy** - the collinearity equations and depth from parallax
4. **Structure from motion** - and bundle adjustment
5. **Ground control points** - georeferencing to a real CRS
6. **Dense matching** - from sparse tie points to dense point clouds
7. **DSM and DTM** - surface versus bare-earth terrain models
8. **Orthomosaics and workflows** - Pix4D and OpenDroneMap end to end

The thread through all of it: a pixel is a **ray** in space. Photogrammetry
is the discipline of intersecting those rays precisely enough to trust the
numbers that fall out.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is photogrammetry, fundamentally?",
                    (
                        opt("A way to compress photographs for storage"),
                        opt(
                            "The science of making reliable measurements of the 3D world "
                            "from photographs taken from different positions",
                            correct=True,
                        ),
                        opt("A photo-editing technique for removing lens blur"),
                        opt("A method for colour-correcting drone imagery"),
                    ),
                    "If you know how the camera behaves and where it was, overlapping "
                    "photos let you recover 3D coordinates.",
                ),
                q(
                    "What does this course say a single image pixel represents in space?",
                    (
                        opt("A fixed 3D point at a known distance"),
                        opt("A colour value only, with no geometric meaning"),
                        opt(
                            "A ray - a direction in space; 3D structure comes from "
                            "intersecting rays from multiple views",
                            correct=True,
                        ),
                        opt("A pixel is always exactly one metre on the ground"),
                    ),
                    "One pixel fixes a direction, not a distance; two or more rays "
                    "intersect to fix a 3D point.",
                ),
            ),
        ),
        # -- 1. Pinhole model ------------------------------------------
        _t(
            "Camera geometry and the pinhole model",
            "10 min",
            """# Camera geometry and the pinhole model

Every photogrammetric measurement starts with a model of how a 3D point
becomes a 2D pixel. The simplest faithful model is the **pinhole camera**:
light from a scene point passes through a single point (the **projective
centre**) and lands on the image plane. A point far from the camera
projects smaller; the governing constant is the **focal length** f.

For a point at camera-frame coordinates (X, Y, Z), the ideal perspective
projection onto the image plane is:

```text
x = f * X / Z
y = f * Y / Z
```

Divide by depth Z - that division is what makes projection **non-linear**
and is why distant objects shrink. To make the algebra linear we use
**homogeneous coordinates** and stack the parameters into a 3x3 **intrinsic
matrix** K, which maps a camera-frame ray to pixel coordinates:

```text
        [ fx   s   cx ]
    K = [  0  fy   cy ]
        [  0   0    1 ]

    s * [u v 1]^T = K * [X Y Z]^T   (point already in the camera frame)
```

Here **fx, fy** are focal length in pixels, **cx, cy** are the **principal
point** (where the optical axis meets the sensor, near the image centre),
and **s** is skew (almost always 0). Combined with the camera's position
and rotation in the world, the full mapping is the 3x4 **projection
matrix** P = K [R | t].

```mermaid
graph LR
    WORLD["World point X Y Z"] --> POSE["Rotation and translation R t"]
    POSE --> CAM["Camera frame coordinates"]
    CAM --> DIV["Divide by depth Z"]
    DIV --> K["Intrinsics K applies fx fy cx cy"]
    K --> PIX["Pixel u v"]
```

Remember: the pinhole model turns a 3D point into a pixel by a rotation, a
translation, a perspective division, and an intrinsic scaling. Every later
step either estimates these parameters or inverts this mapping.
""",
        ),
        quiz_lesson(
            "Quiz: Camera geometry and the pinhole model",
            (
                q(
                    "In the pinhole model, why does a distant object appear smaller in the image?",
                    (
                        opt("Because the sensor loses resolution with distance"),
                        opt(
                            "Because projection divides by depth Z (x = f X / Z), so "
                            "larger Z yields smaller image coordinates",
                            correct=True,
                        ),
                        opt("Because focal length decreases with distance"),
                        opt("Because the lens blurs faraway points"),
                    ),
                    "The perspective division by Z is exactly what shrinks distant "
                    "objects and makes projection non-linear.",
                ),
                q(
                    "What do the entries cx and cy in the intrinsic matrix K represent?",
                    (
                        opt("The camera position in world coordinates"),
                        opt(
                            "The principal point - where the optical axis meets the "
                            "sensor, near the image centre",
                            correct=True,
                        ),
                        opt("The rotation of the camera"),
                        opt("The pixel size in millimetres"),
                    ),
                    "K holds the intrinsics: fx, fy (focal length in pixels) and cx, cy "
                    "(the principal point).",
                ),
                q(
                    "What does the full projection matrix P = K [R | t] combine?",
                    (
                        opt("Two images into one panorama"),
                        opt(
                            "The intrinsics K with the camera's world orientation R and "
                            "position t, mapping a world point to a pixel",
                            correct=True,
                        ),
                        opt("The red, green and blue channels"),
                        opt("The GPS log with the exposure time"),
                    ),
                    "P encodes both where the camera is (R, t = exterior) and how it "
                    "images (K = interior).",
                ),
            ),
        ),
        # -- 2. Interior and exterior orientation ----------------------
        _t(
            "Interior and exterior orientation",
            "10 min",
            """# Interior and exterior orientation

Photogrammetry splits a camera's parameters into two groups, and knowing
which is which is essential.

**Interior orientation (IO)** describes the camera *itself* - the geometry
inside it, independent of where it points:

- **Focal length** (principal distance) and **principal point** (cx, cy).
- **Lens distortion** - real lenses bend straight lines. The dominant term
  is **radial distortion**, modelled by coefficients k1, k2, k3 as a
  function of radius r from the principal point:

```text
    r^2 = (x - cx)^2 + (y - cy)^2
    x_corrected = x * (1 + k1*r^2 + k2*r^4 + k3*r^6)
    y_corrected = y * (1 + k1*r^2 + k2*r^4 + k3*r^6)
```

Finding these values is **camera calibration**. It is done once per
camera/lens (a calibration target, or **self-calibration** solved jointly
during processing).

**Exterior orientation (EO)** describes where the camera *was* for a given
photo - its **pose** in the world:

- **Position** (Xo, Yo, Zo) of the projective centre.
- **Attitude** - three rotation angles **omega, phi, kappa** (roll, pitch,
  yaw), assembled into the rotation matrix R.

So each photo has six EO unknowns (3 position + 3 rotation) plus the shared
IO. Drones give a first guess of EO from **GNSS** (position) and the **IMU**
(attitude); photogrammetry refines them.

```mermaid
graph TD
    CAM["Camera parameters"] --> IO["Interior orientation"]
    CAM --> EO["Exterior orientation"]
    IO --> FOCAL["Focal length and principal point"]
    IO --> DIST["Lens distortion k1 k2 k3"]
    EO --> POS["Position Xo Yo Zo from GNSS"]
    EO --> ATT["Attitude omega phi kappa from IMU"]
```

Remember: interior orientation is the camera's fixed personality; exterior
orientation is where it stood and looked for each shot. You calibrate the
first and solve the second per image.
""",
        ),
        quiz_lesson(
            "Quiz: Interior and exterior orientation",
            (
                q(
                    "Which parameters belong to interior orientation?",
                    (
                        opt("The camera's GPS position and heading"),
                        opt(
                            "Focal length, principal point, and lens distortion - the "
                            "camera's own geometry",
                            correct=True,
                        ),
                        opt("The three rotation angles omega, phi, kappa"),
                        opt("The altitude the drone flew at"),
                    ),
                    "Interior orientation is intrinsic to the camera/lens and is found "
                    "by calibration.",
                ),
                q(
                    "How many exterior-orientation unknowns does each photograph have?",
                    (
                        opt("Two - just latitude and longitude"),
                        opt("Nine - the full rotation matrix entries"),
                        opt(
                            "Six - three position (Xo, Yo, Zo) and three rotation "
                            "(omega, phi, kappa)",
                            correct=True,
                        ),
                        opt("Zero - the drone measures them exactly"),
                    ),
                    "Pose = 3 position + 3 attitude = 6 EO unknowns per image; GNSS/IMU "
                    "give a starting guess.",
                ),
                q(
                    "What does radial lens distortion cause, and how is it modelled?",
                    (
                        opt("It shifts colours; corrected with a white balance"),
                        opt(
                            "It bends straight lines; modelled with coefficients k1, k2, "
                            "k3 as a polynomial in radius from the principal point",
                            correct=True,
                        ),
                        opt("It blurs the image; corrected by sharpening"),
                        opt("It changes exposure; corrected with the histogram"),
                    ),
                    "Radial distortion is a function of r; the k1 r^2 + k2 r^4 + k3 r^6 "
                    "terms undo the bending.",
                ),
            ),
        ),
        # -- 3. Stereoscopy and collinearity ---------------------------
        _t(
            "Stereoscopy and the collinearity equations",
            "11 min",
            """# Stereoscopy and the collinearity equations

**Stereoscopy** recovers depth the way your two eyes do: the same point
seen from two positions shifts across the image by an amount called
**parallax**, and that shift encodes distance. Near objects shift a lot;
far objects shift little.

For a simple **normal-case stereo pair** (two cameras a baseline **B**
apart, focal length **f**, and a horizontal pixel disparity **d** for a
matched point), depth is a clean inverse relationship:

```text
    Z = f * B / d        depth from disparity
    (small disparity -> far away;  large disparity -> close)
```

The rigorous, general statement of the geometry is the **collinearity
condition**: the object point, the projective centre, and the image point
all lie on **one straight line** (the ray). Written per image with the
rotation matrix elements r11..r33 and projective centre (Xo, Yo, Zo):

```text
    x = -f * ( r11(X-Xo) + r21(Y-Yo) + r31(Z-Zo) )
             / ( r13(X-Xo) + r23(Y-Yo) + r33(Z-Zo) )

    y = -f * ( r12(X-Xo) + r22(Y-Yo) + r32(Z-Zo) )
             / ( r13(X-Xo) + r23(Y-Yo) + r33(Z-Zo) )
```

These two equations per image point are the core of analytical
photogrammetry. Write them for the **same** object point in two overlapping
images and you get four equations in three unknowns (X, Y, Z) - solve them
and the two rays **intersect** at the 3D point. That intersection is
**space intersection** (triangulation). The reverse - solving for the
camera pose from known ground points - is **space resection**.

```mermaid
graph LR
    OBJ["Object point X Y Z"] --> RAY1["Ray to camera one"]
    OBJ --> RAY2["Ray to camera two"]
    RAY1 --> IMG1["Image point in photo one"]
    RAY2 --> IMG2["Image point in photo two"]
    IMG1 --> INT["Collinearity intersects rays"]
    IMG2 --> INT
    INT --> POS["Recovered 3D position"]
```

Remember: disparity gives quick depth for a rectified pair, but the
collinearity equations are the exact, rotation-aware statement that a
pixel, the lens centre, and the world point are collinear - the backbone
of everything that follows.
""",
        ),
        quiz_lesson(
            "Quiz: Stereoscopy and the collinearity equations",
            (
                q(
                    "In normal-case stereo, Z = f * B / d. What happens to depth as "
                    "disparity d gets smaller?",
                    (
                        opt("Depth gets smaller - the point is closer"),
                        opt(
                            "Depth gets larger - the point is farther away",
                            correct=True,
                        ),
                        opt("Depth is unaffected by disparity"),
                        opt("The point moves sideways, not in depth"),
                    ),
                    "Depth is inversely proportional to disparity: small parallax means "
                    "a distant point.",
                ),
                q(
                    "What does the collinearity condition state?",
                    (
                        opt("That all cameras must share the same focal length"),
                        opt(
                            "That the object point, the projective centre, and the image "
                            "point lie on one straight line (one ray)",
                            correct=True,
                        ),
                        opt("That two images must be perfectly parallel"),
                        opt("That colours must be consistent between photos"),
                    ),
                    "Collinearity = the ray from the world point through the lens centre "
                    "hits the image point; it is the exact projection statement.",
                ),
                q(
                    "Intersecting the rays from two images to find a ground point's X, Y, "
                    "Z is called what?",
                    (
                        opt("Space resection"),
                        opt("Space intersection (triangulation)", correct=True),
                        opt("Radiometric calibration"),
                        opt("Orthorectification"),
                    ),
                    "Space intersection recovers the 3D point from known poses; the "
                    "inverse (pose from known points) is space resection.",
                ),
            ),
        ),
        # -- 4. SfM and bundle adjustment ------------------------------
        _t(
            "Structure from motion and bundle adjustment",
            "11 min",
            """# Structure from motion and bundle adjustment

Classical photogrammetry needed known camera poses to start. **Structure
from Motion (SfM)** removes that requirement: from an unordered set of
overlapping photos it solves for **both** the 3D structure of the scene
**and** the motion (pose) of the camera, simultaneously - which is exactly
what a drone survey needs.

The pipeline:

1. **Feature detection** - find distinctive keypoints in each image
   (SIFT, AKAZE) that survive scale and rotation changes.
2. **Feature matching** - match keypoints between overlapping images; a
   real-world point matched across many images is a **tie point**.
3. **Incremental reconstruction** - start from a good image pair, estimate
   its relative pose, triangulate points, then add images one by one,
   resecting each new camera and triangulating new points.
4. **Bundle adjustment** - the refinement that makes it accurate.

**Bundle adjustment (BA)** jointly optimises every camera's IO and EO and
every 3D point's coordinates at once, by minimising **reprojection error**:
the pixel distance between where each 3D point *lands* when projected and
where it was actually *observed*.

```python
# Reprojection error minimised by bundle adjustment (least squares)
# P_i = K_i [R_i | t_i]  projects world point X_j into image i
def reprojection_error(P, cameras, points, observations):
    total = 0.0
    for (i, j, u_obs, v_obs) in observations:  # point j seen in image i
        u, v = project(cameras[i], points[j])  # collinearity forward model
        total += (u - u_obs) ** 2 + (v - v_obs) ** 2
    return total  # BA adjusts cameras + points to minimise this sum
```

The name comes from the **bundles** of light rays from each camera that are
adjusted together until the rays best intersect. The output is a **sparse
point cloud** (the tie points) plus refined camera poses and calibration -
the geometric skeleton everything else hangs on.

```mermaid
graph LR
    IMGS["Overlapping images"] --> FEAT["Detect features"]
    FEAT --> MATCH["Match to tie points"]
    MATCH --> INCR["Incremental pose and structure"]
    INCR --> BA["Bundle adjustment"]
    BA --> SPARSE["Sparse cloud and refined poses"]
```

Remember: SfM finds structure and camera motion together from plain photos;
bundle adjustment is the least-squares heart that minimises reprojection
error so the whole block is internally consistent.
""",
        ),
        quiz_lesson(
            "Quiz: Structure from motion and bundle adjustment",
            (
                q(
                    "What does Structure from Motion solve for?",
                    (
                        opt("Only the camera poses, given a known 3D model"),
                        opt(
                            "Both the 3D scene structure and the camera motion (poses) "
                            "simultaneously, from overlapping photos",
                            correct=True,
                        ),
                        opt("Only the 3D structure, given known poses"),
                        opt("The colour balance across the image set"),
                    ),
                    "SfM jointly recovers structure and motion, which is why it works "
                    "from an unordered drone image set.",
                ),
                q(
                    "What quantity does bundle adjustment minimise?",
                    (
                        opt("The number of images in the block"),
                        opt("The GPS error of the drone"),
                        opt(
                            "Reprojection error - the pixel distance between observed "
                            "image points and where the 3D points reproject",
                            correct=True,
                        ),
                        opt("The file size of the point cloud"),
                    ),
                    "BA adjusts all cameras and points together to minimise the summed "
                    "reprojection error.",
                ),
                q(
                    "A real-world point matched across several overlapping images is "
                    "called a what?",
                    (
                        opt("A ground control point"),
                        opt("A tie point", correct=True),
                        opt("A vertex"),
                        opt("A voxel"),
                    ),
                    "Tie points link images together in the bundle; GCPs are different "
                    "(surveyed real-world references).",
                ),
            ),
        ),
        # -- 5. Ground control and georeferencing ----------------------
        _t(
            "Ground control points and georeferencing",
            "10 min",
            """# Ground control points and georeferencing

Bundle adjustment produces a model that is internally consistent but sits
in an **arbitrary coordinate frame** at an arbitrary scale and orientation.
To make measurements mean something on Earth, the block must be tied to a
real **coordinate reference system (CRS)**.

A **Ground Control Point (GCP)** is a feature on the ground whose real-world
coordinates are known precisely (surveyed with **RTK/PPK GNSS**, often to
centimetres) and which is **visible and identifiable** in several images -
a painted target or a sharp natural feature. You mark each GCP in the
images; the software then transforms/constrains the block so those marks
land on the known coordinates.

- **GCPs** fix and check the model geometry.
- **Check points** are surveyed points held *out* of the solution and used
  only to measure the final accuracy.
- **Direct georeferencing** uses the drone's onboard **RTK/PPK** camera
  positions instead of (or with) GCPs.

Georeferencing means choosing a CRS. Common choices:

```text
    EPSG:4326   WGS84 geographic (lat, lon in degrees) - for storage
    EPSG:32633  WGS84 / UTM zone 33N (metres) - for measuring
    (projected UTM is preferred for area/distance; degrees are not metres)
```

A rigid similarity (**Helmert**) transform - rotation, translation, uniform
scale - aligns the arbitrary block to the GCPs:

```text
    [X_world]         [X_model]   [tx]
    [Y_world] = s R * [Y_model] + [ty]     7 parameters:
    [Z_world]         [Z_model]   [tz]     3 rotation, 3 translation, 1 scale
```

```mermaid
graph TD
    BLOCK["Bundle block arbitrary frame"] --> GCP["Mark GCPs in images"]
    GCP --> SURVEY["Surveyed RTK coordinates"]
    SURVEY --> TRANSFORM["Similarity transform to CRS"]
    TRANSFORM --> GEO["Georeferenced model in EPSG code"]
    GEO --> CHECK["Check points measure accuracy"]
```

Remember: SfM gives you shape; ground control gives you **scale, position,
and orientation on Earth**, plus independent check points to prove the
accuracy you claim.
""",
        ),
        quiz_lesson(
            "Quiz: Ground control points and georeferencing",
            (
                q(
                    "Why is a raw SfM/bundle-adjustment result not yet usable for "
                    "real-world measurement?",
                    (
                        opt("It has the wrong colours"),
                        opt(
                            "It sits in an arbitrary frame with arbitrary scale and "
                            "orientation - it must be tied to a real CRS",
                            correct=True,
                        ),
                        opt("It contains too many points"),
                        opt("It is always upside down"),
                    ),
                    "The block is internally consistent but not georeferenced; GCPs or "
                    "RTK positions fix scale, position and orientation.",
                ),
                q(
                    "What is the role of a check point (as opposed to a control point)?",
                    (
                        opt("It is used to constrain the bundle adjustment"),
                        opt(
                            "It is held out of the solution and used only to measure the "
                            "final accuracy independently",
                            correct=True,
                        ),
                        opt("It marks the drone's takeoff location"),
                        opt("It sets the image exposure"),
                    ),
                    "GCPs go into the solution; check points stay out so their residuals "
                    "are an honest accuracy estimate.",
                ),
                q(
                    "Why project to a UTM CRS such as EPSG:32633 rather than measuring "
                    "in EPSG:4326?",
                    (
                        opt("Because EPSG:4326 cannot store elevation"),
                        opt(
                            "UTM coordinates are in metres, so distances and areas are "
                            "measured directly; EPSG:4326 is in degrees",
                            correct=True,
                        ),
                        opt("Because EPSG:4326 is not supported by drones"),
                        opt("Because UTM has no distortion anywhere on Earth"),
                    ),
                    "Projected CRSs (UTM) give metric coordinates; geographic degrees are "
                    "not a linear distance unit.",
                ),
            ),
        ),
        # -- 6. Dense matching -----------------------------------------
        _t(
            "Dense matching and point clouds",
            "10 min",
            """# Dense matching and point clouds

The sparse cloud from bundle adjustment has only tie points - thousands of
them, but far too few to model a surface. **Dense matching (Multi-View
Stereo, MVS)** now uses the *solved* camera poses to compute a depth for
**many pixels**, producing a **dense point cloud** with millions or
billions of coloured 3D points.

The key advantage: because the poses are already known from SfM, the
**epipolar geometry** is fixed. For any pixel in one image, its match in
another must lie on a single line (the **epipolar line**), turning a 2D
search into a cheap 1D search along that line.

```python
# Per-pixel depth from a known stereo pair (baseline B, focal f in pixels)
import numpy as np

def depth_from_disparity(disparity, focal_px, baseline_m):
    # disparity is a per-pixel array; 0 means no match found
    depth = np.full_like(disparity, np.nan, dtype=float)
    valid = disparity > 0
    depth[valid] = focal_px * baseline_m / disparity[valid]
    return depth        # Z per pixel; unproject with K to get X, Y, Z
```

Algorithms such as **Semi-Global Matching (SGM)** and PatchMatch-MVS
estimate a disparity/depth for every pixel, enforce smoothness so surfaces
are coherent, then **fuse** the depth maps from all overlapping images into
one consistent point cloud, rejecting points that only one view sees.

Quality depends on:

- **Image overlap** - typically **70-80% front and 60-70% side** so every
  ground point is seen from many angles.
- **Texture** - bland surfaces (smooth water, fresh snow) match poorly.
- **GSD** (Ground Sample Distance) - the ground size of one pixel, which
  sets the finest detail you can resolve:

```text
    GSD = (sensor_pixel_size * flying_height) / focal_length
    e.g. lower flight or longer lens -> smaller GSD -> finer detail
```

```mermaid
graph LR
    POSES["Known poses from SfM"] --> EPI["Epipolar one dimensional search"]
    EPI --> DEPTH["Per pixel depth maps"]
    DEPTH --> FUSE["Fuse across all views"]
    FUSE --> DENSE["Dense coloured point cloud"]
    DENSE --> FILTER["Reject inconsistent points"]
```

Remember: SfM finds where the cameras were; dense matching then exploits
those known poses and epipolar lines to compute depth for nearly every
pixel and fuse it into the point cloud that surfaces and orthos are built
from.
""",
        ),
        quiz_lesson(
            "Quiz: Dense matching and point clouds",
            (
                q(
                    "How does dense matching (MVS) differ from the sparse SfM result?",
                    (
                        opt("It removes the camera poses"),
                        opt(
                            "It uses the already-solved poses to compute depth for many "
                            "pixels, producing a dense cloud of millions of points",
                            correct=True,
                        ),
                        opt("It only keeps the tie points"),
                        opt("It converts the cloud to 2D"),
                    ),
                    "Sparse = tie points from BA; dense = per-pixel depth using the known poses.",
                ),
                q(
                    "Why does knowing the camera poses make dense matching efficient?",
                    (
                        opt("It removes the need for overlapping images"),
                        opt(
                            "Epipolar geometry is fixed, so a pixel's match lies on a "
                            "single line - a 1D instead of 2D search",
                            correct=True,
                        ),
                        opt("It lets the algorithm skip texture entirely"),
                        opt("It makes all pixels the same depth"),
                    ),
                    "Known poses fix the epipolar lines, reducing correspondence to a 1D search.",
                ),
                q(
                    "What does Ground Sample Distance (GSD) determine, and how does lower "
                    "flying height affect it?",
                    (
                        opt("Battery life; lower flight uses more battery"),
                        opt(
                            "The ground size of one pixel and thus the finest detail; "
                            "lower flying height gives a smaller GSD (finer detail)",
                            correct=True,
                        ),
                        opt("The colour depth; height has no effect"),
                        opt("The number of GCPs required; it has no relation to height"),
                    ),
                    "GSD = pixel_size * height / focal_length; fly lower (or use a longer "
                    "lens) for finer resolution.",
                ),
            ),
        ),
        # -- 7. DSM and DTM --------------------------------------------
        _t(
            "Digital surface and terrain models (DSM, DTM)",
            "10 min",
            """# Digital surface and terrain models (DSM, DTM)

A point cloud is millions of scattered 3D points. To measure elevation you
usually want a **raster surface**: a regular grid where each cell holds a
height. Two closely related products, and the difference matters:

- **Digital Surface Model (DSM)** - the elevation of the **top of
  everything**: bare ground plus buildings, tree canopy, vehicles. It is
  the "as-seen" surface, built straight from the highest points.
- **Digital Terrain Model (DTM)**, also called a DEM in many contexts - the
  **bare-earth** surface with buildings and vegetation removed, as if the
  ground were stripped naked.

You get a DTM from a DSM (or point cloud) by **ground filtering**:
classifying which points are ground and interpolating a surface through
only those, discarding the rest.

```text
    DSM  = top of canopy / rooftops / ground  (everything)
    DTM  = bare earth only  (objects removed)
    nDSM = DSM - DTM  = object heights (tree height, building height)
```

That last line is powerful: subtracting the two rasters, cell by cell,
gives a **normalised DSM** - the height of objects *above the ground*, e.g.
the height of every tree or building.

A quick raster subtraction with GDAL:

```python
# nDSM = DSM - DTM using GDAL raster algebra
from osgeo import gdal
import numpy as np

dsm = gdal.Open("dsm.tif").ReadAsArray().astype("float32")
dtm = gdal.Open("dtm.tif").ReadAsArray().astype("float32")
ndsm = np.clip(dsm - dtm, 0, None)   # object heights above ground, >= 0
```

Interpolation methods to grid the points include **TIN** (triangulated
irregular network), **IDW** (inverse distance weighting), and **kriging**.

```mermaid
graph TD
    CLOUD["Dense point cloud"] --> GRID["Rasterise to a grid"]
    GRID --> DSM["DSM top of everything"]
    CLOUD --> FILTER["Ground filtering"]
    FILTER --> DTM["DTM bare earth"]
    DSM --> DIFF["Subtract DSM minus DTM"]
    DTM --> DIFF
    DIFF --> NDSM["nDSM object heights"]
```

Remember: DSM is everything as-seen; DTM is the bare ground; their
difference is how tall the objects are. Choosing the right one depends on
whether you are measuring the landscape or the things standing on it.
""",
        ),
        quiz_lesson(
            "Quiz: Digital surface and terrain models (DSM, DTM)",
            (
                q(
                    "What is the difference between a DSM and a DTM?",
                    (
                        opt("A DSM is 2D and a DTM is 3D"),
                        opt(
                            "A DSM is the top of everything (buildings, canopy, ground); "
                            "a DTM is the bare-earth surface with objects removed",
                            correct=True,
                        ),
                        opt("A DSM has colour and a DTM does not"),
                        opt("They are two names for the same raster"),
                    ),
                    "DSM = as-seen top surface; DTM = bare ground after filtering out objects.",
                ),
                q(
                    "What does the normalised DSM (nDSM = DSM - DTM) give you?",
                    (
                        opt("The colour of each pixel"),
                        opt("The camera positions"),
                        opt(
                            "The height of objects above the ground, such as tree or "
                            "building heights",
                            correct=True,
                        ),
                        opt("The slope of the terrain in degrees"),
                    ),
                    "Subtracting bare earth from the top surface leaves the height of "
                    "whatever stands on the ground.",
                ),
                q(
                    "How is a DTM typically derived from a point cloud or DSM?",
                    (
                        opt("By increasing the image contrast"),
                        opt(
                            "By ground filtering - classifying ground points and "
                            "interpolating a surface through only those",
                            correct=True,
                        ),
                        opt("By deleting every point with colour"),
                        opt("By flying the drone a second time"),
                    ),
                    "Ground filtering separates bare-earth points; interpolation (TIN, "
                    "IDW, kriging) grids them into the DTM.",
                ),
            ),
        ),
        # -- 8. Orthomosaics and workflows -----------------------------
        _t(
            "Orthomosaics and drone mapping workflows (Pix4D, OpenDroneMap)",
            "11 min",
            """# Orthomosaics and drone mapping workflows (Pix4D, OpenDroneMap)

A raw aerial photo has **perspective distortion**: it is a central
projection, so tall objects lean, scale changes across the frame, and you
cannot measure directly on it. An **orthomosaic** fixes this. Using the DSM
and the camera poses, each pixel is reprojected to where it would appear in
a true **orthographic (map) projection** - **orthorectification** - so
every pixel has a constant, correct scale. The rectified images are then
**mosaicked and colour-balanced** into one seamless map you can measure on
directly, exported as a georeferenced **GeoTIFF**.

The full drone mapping workflow ties the whole course together:

1. **Plan the flight** - a grid mission with 75% front / 65% side overlap
   at a height set by the target GSD.
2. **Capture** - nadir (and oblique for 3D) images, logging GNSS/IMU;
   place and survey GCPs.
3. **SfM + bundle adjustment** - align images, refine IO/EO, sparse cloud.
4. **Georeference** - mark GCPs, transform to the project CRS.
5. **Dense matching** - MVS dense point cloud.
6. **DSM / DTM** - rasterise and ground-filter.
7. **Orthomosaic** - orthorectify against the DSM and mosaic.
8. **Deliver** - GeoTIFF ortho + DSM/DTM, LAS/LAZ cloud, textured mesh.

Two standard software stacks run this pipeline:

```text
    Pix4D        commercial (Pix4Dmapper / cloud); polished, GCP tools
    OpenDroneMap open source (ODM / WebODM); CLI + web; free, scriptable
    Both output: georeferenced orthomosaic, DSM, DTM, dense cloud, mesh
```

A minimal OpenDroneMap run is a single command over a folder of images:

```python
# Run OpenDroneMap on a folder of drone images (produces ortho + DSM + DTM)
import subprocess

subprocess.run([
    "docker", "run", "-ti", "--rm",
    "-v", "/data/project:/datasets/code",
    "opendronemap/odm",
    "--project-path", "/datasets",
    "--dsm", "--dtm", "--orthophoto-resolution", "5",  # 5 cm/px ortho
])
```

```mermaid
graph LR
    PLAN["Plan flight and overlap"] --> CAPTURE["Capture images and GCPs"]
    CAPTURE --> SFM["SfM and bundle adjustment"]
    SFM --> GEOREF["Georeference to CRS"]
    GEOREF --> DENSE["Dense point cloud"]
    DENSE --> MODELS["DSM and DTM"]
    MODELS --> ORTHO["Orthomosaic GeoTIFF"]
```

Remember: an orthomosaic is a distortion-free, measurable map made by
orthorectifying every image against the DSM and stitching the results.
Pix4D and OpenDroneMap automate the entire chain - camera geometry, SfM,
bundle adjustment, ground control, dense matching, surfaces - into a
repeatable button-press that turns a folder of drone photos into
survey-grade geospatial products.
""",
        ),
        quiz_lesson(
            "Quiz: Orthomosaics and drone mapping workflows (Pix4D, OpenDroneMap)",
            (
                q(
                    "Why can you not measure distances directly on a single raw aerial photo?",
                    (
                        opt("Because the photo is in black and white"),
                        opt(
                            "It is a central perspective projection - tall objects lean "
                            "and scale varies across the frame",
                            correct=True,
                        ),
                        opt("Because the file is compressed"),
                        opt("Because it lacks GPS metadata"),
                    ),
                    "Perspective distortion means non-constant scale; orthorectification "
                    "fixes it to a true orthographic projection.",
                ),
                q(
                    "What makes an orthomosaic measurable where a raw photo is not?",
                    (
                        opt("It is printed at higher resolution"),
                        opt(
                            "Each pixel is orthorectified against the DSM to a constant "
                            "map scale, then mosaicked into a seamless georeferenced map",
                            correct=True,
                        ),
                        opt("It removes all colour to reduce distortion"),
                        opt("It averages several unrelated flights together"),
                    ),
                    "Orthorectification with the DSM and poses gives every pixel correct, "
                    "constant scale.",
                ),
                q(
                    "How do Pix4D and OpenDroneMap relate?",
                    (
                        opt("They are unrelated tools for different industries"),
                        opt(
                            "Both automate the same photogrammetry pipeline (SfM, BA, "
                            "dense matching, DSM/DTM, ortho); Pix4D is commercial and ODM "
                            "is open source",
                            correct=True,
                        ),
                        opt("Pix4D only plans flights; ODM only edits photos"),
                        opt("OpenDroneMap requires Pix4D to run"),
                    ),
                    "Both output georeferenced ortho, DSM, DTM, cloud and mesh; the "
                    "difference is commercial vs open-source/scriptable.",
                ),
                q(
                    "In the end-to-end workflow, which step must precede orthomosaic generation?",
                    (
                        opt("Deleting the GCPs"),
                        opt(
                            "Producing the DSM, because orthorectification reprojects "
                            "pixels using the surface model",
                            correct=True,
                        ),
                        opt("Compressing the images to JPEG"),
                        opt("Turning off the GNSS log"),
                    ),
                    "The ortho is rectified against the DSM, so the surface model must "
                    "exist first.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In the pinhole model, what causes distant objects to appear smaller?",
                    (
                        opt("Lens distortion coefficients"),
                        opt(
                            "The perspective division by depth Z in x = f X / Z",
                            correct=True,
                        ),
                        opt("The principal point offset"),
                        opt("The rotation matrix R"),
                    ),
                    "Dividing by Z is the non-linear heart of perspective projection.",
                ),
                q(
                    "Which parameters are interior orientation versus exterior orientation?",
                    (
                        opt("Interior = position and attitude; exterior = focal length"),
                        opt(
                            "Interior = focal length, principal point, distortion; "
                            "exterior = position (Xo, Yo, Zo) and attitude (omega, phi, kappa)",
                            correct=True,
                        ),
                        opt("Both describe only the lens"),
                        opt("Interior = GNSS; exterior = IMU only"),
                    ),
                    "IO is the camera's own geometry; EO is where each photo was taken.",
                ),
                q(
                    "The collinearity equations express which condition?",
                    (
                        opt("That two images have equal exposure"),
                        opt(
                            "That the object point, the projective centre, and the image "
                            "point are collinear (on one ray)",
                            correct=True,
                        ),
                        opt("That the drone flew in a straight line"),
                        opt("That focal length equals baseline"),
                    ),
                    "Collinearity is the exact, rotation-aware statement of projection.",
                ),
                q(
                    "For a normal-case stereo pair, depth relates to disparity how?",
                    (
                        opt("Z = f * B * d (proportional to disparity)"),
                        opt(
                            "Z = f * B / d (inversely proportional to disparity)",
                            correct=True,
                        ),
                        opt("Z = d / (f * B)"),
                        opt("Depth is independent of disparity"),
                    ),
                    "Small disparity means a far point; depth is inversely proportional "
                    "to disparity.",
                ),
                q(
                    "What does bundle adjustment minimise, and over what does it optimise?",
                    (
                        opt("File size, over the image list"),
                        opt(
                            "Reprojection error, jointly over all camera parameters and "
                            "all 3D point coordinates",
                            correct=True,
                        ),
                        opt("GPS drift, over the flight log only"),
                        opt("Colour difference, over the pixels only"),
                    ),
                    "BA is the least-squares core adjusting cameras and points together "
                    "to minimise reprojection error.",
                ),
                q(
                    "Why are ground control points needed after bundle adjustment?",
                    (
                        opt("To make the images sharper"),
                        opt(
                            "The block is in an arbitrary frame; GCPs tie it to a real "
                            "CRS, fixing scale, position and orientation on Earth",
                            correct=True,
                        ),
                        opt("To reduce the number of tie points"),
                        opt("To speed up feature matching"),
                    ),
                    "SfM gives shape; GCPs give georeferenced scale, position and "
                    "orientation - with check points to prove accuracy.",
                ),
                q(
                    "What does dense matching (MVS) produce, and what does it exploit to "
                    "do so efficiently?",
                    (
                        opt("A sparse cloud, by ignoring the poses"),
                        opt(
                            "A dense point cloud, by using the known poses so matches lie "
                            "on epipolar lines (a 1D search)",
                            correct=True,
                        ),
                        opt("A 2D histogram, by averaging colours"),
                        opt("A textured mesh, by skipping depth estimation"),
                    ),
                    "Known poses fix epipolar geometry, enabling per-pixel depth and a "
                    "dense cloud.",
                ),
                q(
                    "The normalised DSM (nDSM = DSM - DTM) represents what?",
                    (
                        opt("The bare-earth elevation"),
                        opt("The top-of-canopy elevation"),
                        opt(
                            "The height of objects above the ground (e.g. tree or building height)",
                            correct=True,
                        ),
                        opt("The slope of the terrain"),
                    ),
                    "DSM minus DTM leaves how tall the objects standing on the ground are.",
                ),
                q(
                    "What is orthorectification, in the context of building an orthomosaic?",
                    (
                        opt("Colour-balancing the images before stitching"),
                        opt(
                            "Reprojecting each image pixel using the DSM and camera pose "
                            "to a true orthographic projection of constant scale",
                            correct=True,
                        ),
                        opt("Compressing the mosaic to a smaller file"),
                        opt("Detecting features for the bundle adjustment"),
                    ),
                    "Orthorectification removes perspective distortion so every pixel has "
                    "correct, constant scale and is measurable.",
                ),
                q(
                    "How do Pix4D and OpenDroneMap fit into the drone mapping workflow?",
                    (
                        opt("They only plan the flight path"),
                        opt(
                            "They automate the full pipeline - SfM, bundle adjustment, "
                            "georeferencing, dense matching, DSM/DTM, and orthomosaic - "
                            "Pix4D commercial, ODM open source",
                            correct=True,
                        ),
                        opt("They replace the need for any camera geometry"),
                        opt("They only convert coordinate systems"),
                    ),
                    "Both turn a folder of photos into survey-grade ortho, DSM, DTM, "
                    "cloud and mesh through the same photogrammetric chain.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PHOTOGRAMMETRY_DRONE_MAPPING_COURSES: tuple[SeedCourse, ...] = (_PHOTOGRAMMETRY_DRONE_MAPPING,)
