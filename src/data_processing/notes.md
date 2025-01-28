## Model Training Progression

Test 1: 46.38%

- Small Dataset
- SVM Model
- Features included: mfcc

Test 2: 60.98%

- Medium Dataset
- SVM Model
- Features included: mfcc

Test 3: 62.42%

- Medium Dataset
- SVM Model
- Features included: mfcc, chroma_cens, tonnetz, spectral_contrast, spectral_centroid, spectral_bandwidth, spectral_rolloff, rmse, zcr

Test 4: 62.30%

- Same Dataset
- Same Model
- Same Features
- Feature Selection Technique: PCA (Principal Component Analysis)

Test 5: 61.80%

- Same Dataset
- Same Model
- Same Features
- Feature Selection Technique: PCA and Lasso
- Selected 146 features from 162

Test 6: 62.38%

- Same Dataset
- Same Model
- Same Features
- Feature Selection Technique: PCA and Lasso
- Selected 240 features from 243

Test 7: 58.80%

- Same Dataset
- Random Forest Model
- Same Features
- Feature Selectionm Technique: None

Test 8:

- Same Dataset
- Random Forest Model
- Same Features
- Feature Selectionm Technique: PCA and Lasso
