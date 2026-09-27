# Ghi chú học tập

## Phase 0: Môi trường

### python và pip
- `python` là trình thông dịch, dùng để chạy code.
- `pip` là trình quản lý gói, dùng để cài thư viện từ PyPI.
- Trên máy này, `python` và `python3` là một.

### venv (virtual environment)
- Mỗi project có một bản Python + pip riêng, cô lập với hệ thống và với project khác, nên các phiên bản thư viện không đụng nhau.
- Tạo: `python -m venv .venv`
- Bật: `source .venv/bin/activate`. Kiểm tra bằng `which python`, kết quả phải trỏ vào `.venv/bin/python`.
- venv chỉ bật trong terminal hiện tại. Mở terminal mới thì phải `activate` lại.
- `python -m venv` tự tạo file `.venv/.gitignore` chứa `*`, nên Git tự bỏ qua thư mục này.

### Đừng nhầm
- `.venv`: thư mục môi trường ảo.
- `.env`: file chứa biến môi trường và secret (mật khẩu, API key). **Không bao giờ commit file này.**
- `uv`: công cụ thay thế pip + venv, nhanh hơn. `conda` chủ yếu dùng cho Data Science.

### Bài học từ lỗi `.venv-1`
- Trộn `uv` với `venv` + `pip` đã tạo ra venv thứ hai. FastAPI bị cài vào đó, còn `requirements.txt` thì rỗng.
- Trong lúc học chỉ dùng **một** công cụ: `venv` + `pip`.
- Không nhớ đã gõ lệnh gì thì tra: `history | grep <từ khóa>`

## Git

### 3 khu vực
1. **Working directory**: file đang sửa.
2. **Staging area**: thay đổi đã `git add`, được chọn cho commit tiếp theo.
3. **Repository**: thay đổi đã `git commit`, lưu vào lịch sử.

- `git diff`: xem thay đổi chưa add.
- `git diff --staged`: xem thay đổi đã add nhưng chưa commit.
- Có staging để **chọn** thay đổi nào vào commit. Nhờ vậy mỗi commit làm đúng một việc.

### git status và git log
- `git status`: **bây giờ** đang có gì chưa commit. Nhìn khu vực [1] và [2].
- `git log`: **lịch sử** các commit đã làm. Nhìn khu vực [3].
- Commit xong thì thay đổi biến khỏi `status` và xuất hiện trong `log`.
- `git status --short`: cột trái là staging, cột phải là working directory.
  - `M  file`: đã add
  - ` M file`: đã sửa, chưa add
  - `?? file`: file mới, Git chưa theo dõi
- Prompt terminal: `+` là có thay đổi trong staging, `!` là có thay đổi chưa add, `?` là có file mới chưa theo dõi.

### Branch và merge
- Branch là **một cái nhãn trỏ vào một commit**. Commit mới thì nhãn tự dịch lên.
- `main` giữ code ổn định. Tính năng mới làm trên nhánh riêng, xong mới gộp vào.
- `git switch -c <tên>`: tạo nhánh mới rồi chuyển sang. `git switch <tên>`: chuyển nhánh.
- Switch nhánh thì Git thay nội dung file bằng bản chụp của nhánh đó. Code không mất, nó nằm ở nhánh kia.
- Chỉ switch khi `git status` sạch.
- Nhánh mới push lần đầu cũng cần `-u`: `git push -u origin <tên>`
- `git merge <nhánh>`: gộp nhánh đó vào nhánh đang đứng. **Fast-forward** là khi `main` không có commit mới, Git chỉ cần dời nhãn `main` lên.
- Merge xong nhớ push cả `main`. `ahead 1` trong `git branch -vv` là còn 1 commit chưa push.
- `git branch -d`: xóa nhánh đã merge. `-D`: xóa nhánh chưa merge (bắt buộc xác nhận).
- Lỗi `src refspec ... does not match any`: tên nhánh gõ sai. Dùng `Tab` để tự điền.

### Hoàn tác
- Sửa file `a` rồi `git restore a` thì **mất hết** thay đổi, file quay về bản đã lưu trong Git. Không giống Ctrl+Z: nó bỏ tất cả một lần, và không hoàn tác được.
- Đã `git add a` rồi `git restore --staged a` thì **hủy add**, thay đổi vẫn còn nguyên trong file.
- Đã add rồi thì `git restore a` không có tác dụng, vì file và staging đang giống nhau. Muốn bỏ hẳn thì `--staged` trước, `restore` sau.
- `git reset --soft HEAD~1`: hủy commit vừa tạo, thay đổi quay về staging. Là chiều ngược lại của `git commit`. **Chỉ dùng khi commit chưa push.**
- `HEAD` là commit đang đứng, `HEAD~1` là commit ngay trước nó.
- Không dùng `git restore .` khi chưa chắc chắn, vì nó áp dụng cho mọi file.

### .gitignore
- Danh sách những thứ không bao giờ đưa vào Git.
- Vẫn cần có dù venv tự ẩn, vì còn `.env`, `__pycache__/`, `*.pyc`, và vì quy tắc phải đi theo project, không phụ thuộc vào máy của ai.
- Tên phải khớp chính xác: `.venv/` khác `venv`. `./` không phải cú pháp của gitignore.

### GitHub
- SSH key là một cặp khóa:
  - `id_ed25519` là khóa riêng. Giữ bí mật, không chia sẻ.
  - `id_ed25519.pub` là khóa công khai, đưa cho GitHub.
- Test kết nối: `ssh -T git@github.com`
- `git remote add origin <url>` nối repo local với GitHub.
- `git push -u origin main`: `-u` là `--set-upstream`. Sau lần này chỉ cần gõ `git push`.
- Thứ tự tạo venv hay `git init` trước không quan trọng, vì Git chỉ nhìn trạng thái hiện tại của thư mục.
- `git log` báo lỗi `less` là do thiếu pager. Cài bằng `sudo pacman -S less`.

## Phase 1: Python

### Decorator
- Là một hàm nhận vào một hàm, rồi trả về một hàm mới.
- `@log_call` đặt trên `def greet` tương đương `greet = log_call(greet)`.
- Hàm cũng là object, nên truyền được như tham số và có thuộc tính như `__name__`.
- Sau khi gắn decorator, cái tên `greet` trỏ vào `wrapper`, không còn là hàm gốc.

### functools.wraps
- `@wraps(func)` đặt trên `def wrapper`.
- Nó chép thông tin của hàm gốc (`__name__`, `__doc__`...) sang `wrapper`.
- Nó **không** thay đổi cách hàm chạy. Nó chỉ thay đổi câu trả lời khi có ai hỏi thông tin về hàm (log, traceback, FastAPI).

### *args và **kwargs
- `*args`: gom tham số **không có tên** vào một tuple.
- `**kwargs`: gom tham số **dạng `tên=giá_trị`** vào một dict.
- Trong `def wrapper(*args, **kwargs)`, dấu `*` là **gom**. Trong `func(*args, **kwargs)`, dấu `*` là **mở ra**.
- Nhờ vậy decorator dùng được cho mọi hàm, bất kể hàm có bao nhiêu tham số.

## FastAPI

### Bài 1: Hello API
- Cài: `pip install "fastapi[standard]"`. Gói này kèm `uvicorn`, là server nhận request từ mạng.
- Lưu danh sách thư viện: `pip freeze > requirements.txt`
- Chạy: `fastapi dev app.py`
- `@app.get("/")` **ghi** vào bảng route (GET + `/` → `home`) lúc app khởi động. Nó không chạy `home` ngay.
- Khi có request tới, FastAPI tra bảng, gọi hàm tương ứng, rồi đổi dict thành JSON.
- `app.get("/")` được gọi trước và trả về một decorator. Vì cần truyền đường dẫn vào nên mới có dấu ngoặc.
- Đường dẫn không có trong bảng thì trả về **404**. Thành công thì trả về **200**.
- `/docs` được sinh tự động từ bảng route.

### Bài 2: Path parameter và type hint (đang làm)
- `/notes/{note_id}`: phần `{note_id}` thay đổi được.
- `note_id: int` là type hint. Python thường không kiểm tra type hint, nhưng FastAPI thì có.
- JSON chỉ chứa được số, chuỗi, list, dict, true/false, null. Vì vậy `type(x)` phải bọc trong `str()`.
- Kết quả thí nghiệm `/notes/abc` và khi bỏ `: int`: *(chưa làm)*

### Bài 3: POST và Pydantic
- **GET** để lấy dữ liệu, thông tin nằm trên URL. **POST** để tạo mới, dữ liệu nằm trong **body** dạng JSON.
- `class NoteCreate(BaseModel)` mô tả hình dạng dữ liệu bằng type hint. `NoteCreate` **kế thừa** `BaseModel` nên có sẵn khả năng kiểm tra dữ liệu.
- Body gửi lên sai hình dạng (thiếu field, sai kiểu) thì FastAPI tự trả **422**.
- Lưu note trong list thì restart server là mất, vì list nằm trong RAM. Cần database để lưu xuống ổ đĩa.
- Test POST ở `/docs`: "Try it out", sửa body, "Execute".

### Bài 4: id, 404, xóa
- `class Note(NoteCreate)` thêm `id`. Tách 2 class vì người dùng không được tự đặt id: gửi lên `NoteCreate`, server trả về `Note`.
- `status_code=201`: mã chuẩn khi tạo mới thành công.
- `Note(id=next_id, **payload.model_dump())`: `model_dump()` đổi object thành dict, rồi `**` mở dict ra thành tham số có tên.
- `global next_id`: bắt buộc có thì mới gán lại được biến nằm ngoài hàm.
- `raise HTTPException(status_code=404, detail=...)`: dừng hàm và trả lỗi 404.
- **Bug đã gặp:** thiếu `return` sau `notes.remove(note)` nên hàm chạy tiếp tới `raise`. Note bị xóa thật nhưng client lại nhận 404. `return` làm hàm thoát ngay.

### Kiểu trả về `->`
- `-> Note` khai báo hàm trả về gì. Nó không sửa bug, chỉ mô tả. `-> None` nghĩa là không trả về gì.
- Python không bắt buộc có `->`. Nhưng với route FastAPI thì **luôn ghi**, vì FastAPI dùng nó để:
  1. Hiện hình dạng response trên `/docs`
  2. Kiểm tra dữ liệu trả về
  3. **Lọc bỏ field thừa**. Ví dụ `-> UserPublic` thì không bao giờ lộ `password_hash`.

## Tự kiểm tra
Trả lời bằng lời của bạn, không nhìn phần ghi chú ở trên:
1. Tại sao cần venv?
2. `git diff` và `git diff --staged` khác nhau ở đâu?
3. Sau khi gắn `@log_call`, `greet.__name__` ra gì? Vì sao? `@wraps` sửa điều đó bằng cách nào?
4. `show(1, x=2)` thì `args` và `kwargs` là gì?
5. `@app.get("/")` làm gì lúc khởi động app, và làm gì lúc có request tới?
6. `git status` và `git log` khác nhau ở đâu?
7. Đã add file rồi, muốn bỏ hẳn thay đổi thì làm mấy bước, lệnh gì?
8. Vì sao `delete_note` trả về 404 dù đã xóa note, khi thiếu `return`?

