## ORM 목록

1. __board.user:  게시글을 작성한 유저 (1:n)__
2. __board.like_users: 게시글을 좋아요한 유저들(m:n)__
3. __user.board_set: 유저가 작성한 게시글들(1:n)__
4. __user.like_boards: 유저가 좋아요한 게시글들(m:n) - related_name__





## LIKE

- user 는 여러 board에 like 할 수 있음
- board는 여러 user로부터 like 받을 수 있음
- User : Board = M:N



- 나(board)를 좋아요 한 모든 유저

  - __board.like_users.all()__

  - 내가 쓴 모든 글 가져오기

    ```python
    user.board_set.all() # 1:1관계 user에서 사용 중
    ```

  - 내가 좋아요한 모든 글들 

    ```python
    user.like_boards.all() # 역참조의 오류로 인해 무조건 related_name 사용
    ```

    




## FOLLOW

- User : User = M:N