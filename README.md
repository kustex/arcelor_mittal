# ArcelorMittal – Predicting Width Constrictions (BeCode project)

## Problem
During hot rolling, a **width constriction** can occur around **140–170 m** from the head when the strip is picked up by the downcoiler. B4 (before downcoiler) does **not** show the constriction, B5 (after downcoiler) **does**. The goal is to **predict the risk of constriction in advance** using only data known *a priori* (chemical composition, hardness, width, thickness, etc.). *(Context distilled from the project brief / slides.)*

## Data
- **SignalExport B4/B5**: one CSV per coil and measurement (B4/B5), with length points (0–200 m) and width values (some cleaning needed; zeros at start).
- **CoilData.csv**: per-coil features known before processing:  
  Hardness(1/2), Width, Thickness, **chemical composition** (c, mn, si, …), and categorical **analyse** (first 3 digits = main group).  
  *Per brief we avoid using “Furnace number”, “Thickness profile”, and temperatures.*

## Label creation (ground truth)
See `get_contracted_coils.py`:
1. For each coil, read B4 and B5 using `csv_reader.csv_to_df()`; interpolate both curves to 0.1 m over 0–200 m.
2. Compute **|B4−B5|** over **[140 m, 170 m]** and take the **max absolute difference** per coil.
3. Mark coils in the **top 5%** of that max-difference distribution as **contracted = 1**; others **0**.  
   The resulting labels are written to `output.csv` and joined back to `CoilData.csv` by `coil`.

> This mirrors the domain rule from the slides: constriction reveals as a B5 deviation near 140–170 m relative to B4.

## Feature engineering & preprocessing (from `model.ipynb`)
- Drop: `coil`, `analyse`, `analyse_main`, `furnace Number`, `Temperature before/after finishing mill`.
- Clean **Thickness profile** (strip “*******”), keep non-negative; later excluded from the final training set.
- **Log-transform** the first 19 numeric columns; replace `-inf` with the log of the per-column smallest positive value/1000.
- **One-hot encode** the 3-digit `analyse_main` category.
- **Class balance** by undersampling the majority class to match the number of contracted coils.
- Train/validation split: `train_test_split(test_size=0.2, random_state=42)`.

## Models & search space
We grid-searched 6 classifiers (3-fold CV, scoring=accuracy):
- Logistic Regression (`multi_class` ∈ {auto, ovr, multinomial}, `max_iter=1000`)
- Decision Tree (`criterion` ∈ {gini, entropy}, `max_depth` ∈ {3,6,9,12})
- Random Forest (`criterion` ∈ {gini, entropy}, `max_depth` ∈ {3,6,9,12}, `min_samples_split` ∈ {3,6,9,12})
- SVM (`kernel` ∈ {linear, rbf}, `C` ∈ {3,6,9,12})
- GaussianNB (`var_smoothing` ∈ logspace[0…1e−9])
- BernoulliNB (`alpha` ∈ [0.1 … 1.0])

## Results (test set)
### Round A — All engineered features
**Best:** Random Forest — params `{'criterion': 'entropy', 'max_depth': 12, 'min_samples_split': 6}`  
- Accuracy: 0.806
- Precision (contracted=1): 0.857
- Recall (contracted=1): 0.746
- F1 (contracted=1): 0.798
- Confusion Matrix (rows=true [0,1], cols=pred [0,1]): [[469, 71], [145, 426]] (N=1111)

Reference (other models, test accuracy):  
- Decision Tree ≈ 0.796; Logistic Regression ≈ 0.773; SVM (rbf) ≈ 0.748; GaussianNB ≈ 0.658; BernoulliNB ≈ 0.653.

### Round B — Top 20 features by RF importance
**Best:** Random Forest — params `{'criterion': 'entropy', 'max_depth': 12, 'min_samples_split': 3}`  
- Accuracy: 0.794
- Precision (contracted=1): 0.820
- Recall (contracted=1): 0.760
- F1 (contracted=1): 0.789
- Confusion Matrix (rows=true [0,1], cols=pred [0,1]): [[455, 94], [135, 427]] (N=1111)

*(Slightly lower overall accuracy vs Round A, with a small uptick in recall.)*

The best grid-search pipeline is saved as **`best_grid_search_pipeline.pkl`**.

## Notebooks / scripts
- **`dev.ipynb`** — quick exploration & visualization of B4 vs B5 for specific coils.
- **`model.ipynb`** — full preprocessing, balancing, grid search over models, ROC curves, feature importances.
- **`csv_reader.py`** — helper to parse B4/B5 CSVs into `length_p` and `values` series.
- **`get_contracted_coils.py`** — label creation pipeline; writes `output.csv` (coil IDs with highest constriction risk).

## How to reproduce
1. Place raw data under `data/` as in the notebooks (e.g., `data/SignalExport/*.csv`, `data/CoilData.csv`).
2. Run `python get_contracted_coils.py` to generate `output.csv` labels.
3. Open `model.ipynb` and run all cells to train models and export the best pipeline.
4. (Optional) Use `dev.ipynb` to visualize B4/B5 around 140–170 m for specific coils.

## Next steps
- Try **class-weighted** models or **SMOTE** to avoid undersampling signal.
- Add **threshold tuning** to trade precision vs recall for operations.
- Explore **time/position-aware features** from the B4/B5 curves (e.g., area under |B4−B5| over 140–170 m).
- Validate on a **holdout period** or with **K-Fold** CV for robust generalization.
