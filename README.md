
### 데이터 셋

- [셀렉트스타 음식 데이터](https://open.selectstar.ai/ko/?page_id=5976)
    - 1024 X 1024 픽셀 이상의 고해상도 이미지
    - 100개의 음식 클래스 당 1000개의 사진으로 구성
    - 계층 구조가 정의된 음식 재료 레이블링 (json)
    - 해당 데이터 셋을 가공해 112종류의 재료 데이터를 17개의 알레르기 데이터로 변환

93개의 음식 클래스와 17개 종류의 알레르기 유발 재료 클래스

**데이터 폴더 구조**
  ```
    data
    │  data.csv
    │  
    ├─image
    │  ├─baek_sook
    │  │      baek_sook_0001.jpg
    │  │      baek_sook_0002.jpg
    │  │      ...
    │  │
    │  ├─baguette
    │  ├─banh_mi
    │  ...
    │  ├─udon
    │  ├─waffle
    │  └─wolnam_ssam
    │
    └─json
        ├─baek_sook
    		│      1000_korea_baek_sook.json
        │      1001_korea_baek_sook.json
        │      ...
        │
    		├─baguette
        ├─banh_mi
        ...
        ├─udon
        ├─waffle
        └─wolnam_ssam
  ```

## 각 파트의 사용법
[model](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-01/tree/dev/model)

[frontend](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-01/tree/dev/serving/frontend)

[backend](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-01/tree/dev/serving/backend)
