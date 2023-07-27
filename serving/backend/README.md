#모델 서버 실행
Tresnet_m_ml_decoder_recipy_final_latest.pth 파일을 pth 폴더에 넣는다.
pip install -r requirements.txt
python modelserver.py

#서버 실행
server.c에서 모델 서버의 ip를 수정하고 num_model_serv의 값을 변경한다.
gcc server.c -pthread
./a.out 30010