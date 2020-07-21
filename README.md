# mayonnaise-backend

## Introduction
- wecode 9기 수강생들의 2차 클론 프로젝트입니다.
- 프로젝트 기간 : 2020.7.6 ~ 2020.7.17 (2주)
- 6명의 개발자가 함께 협업했습니다. (3 Front-End, 3 Back-End)

## 2차 프로젝트 소개
 피부 수분에 대한 연구를 기초로 한 화장품 브랜드 라네즈(https://www.laneige.com/kr/ko/) 웹사이트 클론 프로젝트


## 데모영상
[![Video Label](https://user-images.githubusercontent.com/60872814/88010998-2c0c1400-cb51-11ea-98d1-f91a9df7674e.png)](https://www.youtube.com/watch?v=xIFB2U80wgc&feature=youtu.be)
 

## 목표
- https://www.laneige.com/kr/ko/ 사이트의 interface와 동일하게 화면 구현하기
- 회원가입/로그인, 소셜로그인, cart, reservation, sms 기능 구현하기
- Back-End API를 통해 데이터를 GET / POST / PUT / DELETE 하기
- (포토) 리뷰 등록 및 삭제
- trello를 사용해 협업하며 매일 정해진 시간에 stand up 미팅 진행하기

## 사용한 기술
- Python: List-complihension
- Django: select_related, prefetch_related, ORM
- Postman: api 문서화
- RESTful API
- unit test
- AWS, Docker

## 기능
- 회원가입 및 로그인 (bcrypt와 jwt를 활용한 access_token 전송)
- 카카오톡 소셜 로그인
- 인가 기능 데코레이터
- 회원별 예약기능 구현
- 상품리스트와 상세페이지 데이터 전송
- 리뷰 등록 및 삭제
- 이미지 업로드 기능 구현
- 페이지네이션 구현
- 제품 검색 기능 구현
- 좌표 값을 통해 맵 마킹
- 각 엔드포인트에 대한 unit test 진행

## postman 문서화
https://documenter.getpostman.com/view/11626571/T17Kd6Jh?version=latest#66aa9de0-fef6-448a-bf8a-f9527d6b5b7b
