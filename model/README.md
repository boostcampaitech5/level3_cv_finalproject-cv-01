## 학습 방법
``` python 
python app.py --dataset_path={데이터가 존재하는 파일의 경로} --save_path={학습된 모델 저장 경로} --model_name={model.py에 존재하는 모델의 class} --seed={지정된 seed} --num_workers={GPU의 workers의 수}  --epochs={epoch} --batch={batch} --resize={resize} --lr={시작 학습률} --eta_min={최종 학습률} --weight_decay={AdamW에서 지정하는 weight_decay}
```

## 파일 구조
``` bash
📦model
 ┣ 📜README.md
 ┣ 📜app.py
 ┣ 📜baseline.ipynb
 ┣ 📜dataset.py
 ┣ 📜inference.ipynb
 ┣ 📜loss.py
 ┣ 📜ml_decoder.py
 ┣ 📜models.py
 ┣ 📜train.py
 ┣ 📜utils.py
 ┗ 📜visualize.ipynb
```

## 모델
모델은 Timm의 모델을 사용했다.
또한, https://github.com/Alibaba-MIIL/ML_Decoder 의 ML_decoder와 ASL Loss를 사용했다.
1. Resnet50
2. Tresnet_m
3. Tresnet_m + ml_decoder
4. Efficientnetv2_s
5. Vit_tiny
6. Vit_small
7. swinv2_cr_tiny

## 최종 모델
Tresnet_m + ML_decoder를 사용하여 학습했다.
### Tresnet
Tresnet은 Resnet50을 변형하여 제작된 모델이며 메모리의 효율적인 사용을 중점적으로 다루며 경량화한 모델이다.
아래 방법론들을 적용하여 경량화 및 성능 향상 그리고 메모리 효율적인 사용을 보여주었다.
1. Space To Depth
2. Novel Block-Type Selection
3. In-Place Activated Batch Normalization
4. Optimized SE(Squeeze-and-Excitation)
5. Anti-Aliasing

### ML_decoder
기존 Global Average Pooling은 여러 객체가 존재하는 Multi-Label의 경우 적합하지 않기 때문에 Attention을 이용하여 더 좋은 결과를 낼 수 있었다.

하지만, 기존 Transformer-Decoder를 사용하게 되면 많은 수의 Class를 갖는 작업을 수행하기엔 굉장히 큰 연산량이 필요하게 된다.

ML-Decoder는 Self-Attention을 제거함으로써 디코더가 입력 쿼리 수에 대해 제곱적인 의존성을 선형으로 줄이면서 연산 복잡성이 효율적으로 감소했다.

또한, Group Decoding을 이용하여 효율적인 메모리 사용, 연산 감소 효과를 얻을수 있으며, 고정된 쿼리를 이용하면서 ZSL(Zero-Shot Learning)을 가능하도록 했다.

### ASL Loss
# ASL Loss

기존 Class Imbalance를 컨트롤하는 Loss Function으로는 Focal Loss가 있다.

Focal Loss는 Cross Entropy Loss를 베이스로 한 Loss function으로 $\gamma$를 조절하면서 더욱 극적인 가중치를 줄 수 있다.($\gamma$=0이면 Cross Entropy Loss)

즉, Focal Loss는 학습하기 어려운 데이터를 가중치를 다르게 주면서 Class Imbalance를 해결하는 방법이다.

하지만, 어려운 데이터를 가중치에 더 큰 가중치를 주게 되고, 상대적으로 학습하기 쉬운 데이터의 Loss가 크다는 단점이 있다.

즉, 학습하기 어려운 Negative 데이터를 Down-weight 하지만 여기서 발생하는 tradeoff 문제를 해결하고자 제작이 된 Loss Function이 Asymmetric Loss이다.

ASL Loss의 경우 Positive, Negative 데이터를 다르게 학습해야한다고 이야기한다.


Focal Loss와 식이 같지만, 다르다.

항상 $r_{+}< r_{-}$로 설정하여 Positive 데이터의 decay weight를 다르게 학습하여 어려운 Positive 데이터를 잘 학습될 수 있도록 하는 것이다.

하지만, 여기서 Imbalance가 매우 큰 상황을 가정한다면 Negative 데이터를 학습이 안되는 경우가 있기 때문에 이를 보완하기위해 hard thresholding를 추가한다.