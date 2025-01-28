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

- Same Model
- Same Features
- Feature Selection: PCA (Principal Component Analysis)

Test 5: 61.80%

- Same Model
- Same Features
- Feature Selection: PCA and Lasso
- Selected 146 features from 162

Test 6: 62.38%

- Same Model
- Same Features
- Feature Selection: PCA and Lasso
- Selected 240 features from 243

Test 7: 58.80%

- Random Forest Model
- Same Features
- Feature Selection: None

Test 8: 51.73%

- Random Forest Model
- Same Features
- Feature Selection: PCA and Lasso

Test 9, 10: 62.18%, 62.38%

- Gradient Boosting Machine Model
- Same Features
- Feature Selection: None

Test 11: 55.97%

- Neural Network Model
- Same Features
- Feature Selection: None

Test 12: 54.49%

- Neural Network Model
- Same Features
- Feature Selection: PCA and Lasso
