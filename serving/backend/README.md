# 모델 서버 실행
1. Tresnet_m_ml_decoder_recipy_final_latest.pth 파일을 pth 폴더에 넣는다.
2. pip install -r requirements.txt
3. python modelserver.py

# 서버 실행
1. server.c에서 모델 서버의 ip를 수정하고 num_model_serv의 값을 변경한다.
2. gcc server.c -pthread
3. ./a.out 30010
