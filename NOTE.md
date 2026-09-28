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

### Pull Request và git pull
- **Pull Request (PR):** lời đề nghị gộp một nhánh vào `main` trên GitHub. Là nơi để review code, bình luận từng dòng, và chạy kiểm tra tự động trước khi gộp.
- Khi đi làm, hầu như không ai `git merge` thẳng vào `main` trên máy. Luôn đi qua PR.
- Mở PR: nút "Compare & pull request", kiểm tra `base: main` ← `compare: <nhánh>`, viết tiêu đề và mô tả.
- Tab "Files changed": tự review như đang đọc code của người khác. Bấm `+` cạnh một dòng để bình luận.
- Merge trên GitHub mặc định tạo **merge commit** (có 2 cha), khác với fast-forward (chỉ dời nhãn).
- `git pull`: **kéo** commit từ GitHub về máy, chiều ngược lại của `git push`. Merge trên GitHub rồi thì phải `pull` thì `main` trên máy mới có code mới.
- GitHub xóa nhánh của nó rồi thì nhánh trên máy vẫn còn, phải tự `git branch -d`.
- `git log --oneline --graph`: vẽ lịch sử thành hình, thấy rõ chỗ nhánh tách ra và nhập lại.

### Merge conflict
- Xảy ra khi 2 nhánh sửa **cùng một dòng** theo 2 cách khác nhau. Git không biết giữ bản nào nên dừng lại và hỏi. Đây không phải lỗi, là chuyện hằng ngày.
- Chỗ nào chỉ một nhánh sửa thì Git tự gộp được. Conflict chỉ nằm đúng ở dòng cả hai cùng sửa.
- Git ghi cả 2 bản vào file:
```
<<<<<<< HEAD
    bản của nhánh đang đứng
=======
    bản của nhánh đang gộp vào
>>>>>>> lesson-7-update
```
- Giải quyết: sửa thành bản cuối cùng mình muốn, **xóa hết 3 dòng marker**, `git add <file>` (báo đã giải quyết xong), rồi `git commit`.
- Quên xóa marker thì file Python bị lỗi cú pháp. Kiểm tra lại bằng cách tìm `<<<<`.
- `UU` trong `git status --short` là đang có conflict (Unmerged). Prompt hiện `(MERGING)` cho tới khi commit xong.
- Tạo nhánh mới khi có thay đổi chưa commit: thay đổi đi theo sang nhánh mới, `main` không bị ảnh hưởng.
- `⇡` trong prompt: có commit chưa push.

### Hoàn tác
- Sửa file `a` rồi `git restore a` thì **mất hết** thay đổi, file quay về bản đã lưu trong Git. Không giống Ctrl+Z: nó bỏ tất cả một lần, và không hoàn tác được.
- Đã `git add a` rồi `git restore --staged a` thì **hủy add**, thay đổi vẫn còn nguyên trong file.
- Đã add rồi thì `git restore a` không có tác dụng, vì file và staging đang giống nhau. Muốn bỏ hẳn thì `--staged` trước, `restore` sau.
- `git reset --soft HEAD~1`: hủy commit vừa tạo, thay đổi quay về staging. Là chiều ngược lại của `git commit`. **Chỉ dùng khi commit chưa push.**
- `HEAD` là commit đang đứng, `HEAD~1` là commit ngay trước nó.
- Không dùng `git restore .` khi chưa chắc chắn, vì nó áp dụng cho mọi file.
- `git revert HEAD`: hủy commit **đã push** bằng cách tạo **commit mới làm ngược lại**. Commit cũ vẫn còn trong log, lịch sử chỉ thêm vào.
- Commit đã push thì không dùng `reset`, vì `reset` viết lại lịch sử. Người khác đã kéo commit đó về sẽ bị lệch, và muốn push thì phải ép (force push), dễ làm mất code của người khác.

- Ví dụ sổ chi tiêu: ghi nhầm "chi 100k". `reset` là xé trang, `revert` là viết thêm dòng "hoàn lại 100k". Sổ dùng chung (đã push) thì chỉ viết thêm, không xé.
- `git show <commit>`: xem chính xác commit đó đã thay đổi gì. Commit revert có các dòng `-`/`+` ngược hẳn với commit gốc.

| Tình huống | Lệnh |
|---|---|
| Sửa file, chưa add | `git restore <file>` |
| Đã add, chưa commit | `git restore --staged <file>` |
| Đã commit, chưa push | `git reset --soft HEAD~1` |
| Đã commit, đã push | `git revert <commit>` |

### Staging là bản chụp
- `git add` chụp file **tại thời điểm đó**. Sửa tiếp sau khi add thì phần sửa mới chưa nằm trong staging.
- `MM file` trong `git status --short`: đã add một bản, rồi lại sửa tiếp. Phải `add` lại trước khi commit.

### Editor của Git
- Git mở editor để viết commit message (khi `git commit` không có `-m`, hoặc khi `git revert`).
- Mặc định là `vi`. Arch không còn cung cấp `vi`, nên revert bị dở dang: thay đổi đã vào staging nhưng chưa có commit.
- Sửa bằng cách chọn editor khác: `git config --global core.editor nano`
- Trong nano: `Ctrl+O`, `Enter` để lưu, `Ctrl+X` để thoát.

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

## PostgreSQL

### Vì sao cần database
- List trong Python nằm trong RAM, tắt chương trình là mất. Database lưu xuống ổ đĩa.

### Service và log
- PostgreSQL là một **server**: chạy nền liên tục, chờ kết nối. Trên Arch, nó được `systemd` quản lý.
- `sudo systemctl restart postgresql`: khởi động lại. `systemctl status postgresql --no-pager`: xem trạng thái.
- Service lỗi thì **đọc log trước, đừng đoán**: `journalctl -u postgresql -n 20 --no-pager`
- Mẹo đọc log: tìm dòng `FATAL` hoặc `ERROR`, rồi đọc các dòng ngay phía trên nó để biết nguyên nhân.

### Port
- Port là số giúp phân biệt các chương trình mạng trên cùng một máy, giống số phòng. uvicorn dùng 8000, PostgreSQL dùng 5432.
- Mỗi port chỉ một chương trình được dùng tại một thời điểm. Lỗi `Address already in use` là port đã bị chiếm.
- Xem ai đang chiếm port: `sudo ss -ltnp | grep 5432`
- **Lỗi đã gặp:** PostgreSQL không chạy được vì một container Docker cũ (`docker-postgres-1` của dự án anphat) đã chiếm port 5432. Đã xóa container đó.
- `docker ps`: xem các container đang chạy. Trước khi xóa container phải biết nó thuộc dự án nào, vì volume có thể chứa dữ liệu thật.

### User và database
- PostgreSQL có hệ thống user riêng, tách biệt với user Linux. User quản trị mặc định là `postgres`.
- Mỗi project nên có user riêng, chỉ có quyền trên database của nó. Không dùng `postgres` cho app.
- Project này dùng: user **`noteuser`**, database **`notesdb`**.
- Vào bằng quyền quản trị: `sudo -iu postgres psql`
- Vào bằng user của project: `psql -h localhost -U noteuser -d notesdb`
- `CREATE DATABASE ... OWNER noteuser`: cho user làm chủ, để được phép tạo bảng.
- Database có sẵn: `postgres` (mặc định), `template0`, `template1` (khuôn mẫu, không đụng vào).

### psql
- Câu SQL phải kết thúc bằng `;`. Quên `;` thì dấu nhắc đổi thành `-#` và chờ gõ tiếp.
- Lệnh bắt đầu bằng `\` là lệnh của psql, không cần `;`: `\l` (liệt kê database), `\conninfo` (đang kết nối thế nào), `\q` (thoát).
- `=#` là superuser, `=>` là user thường.
- `--More--` là đang phân trang. Nhấn `q` để thoát, `Space` để xem tiếp.
- `Password Used | false`: Arch mặc định tin mọi kết nối từ chính máy này (chế độ `trust`). Học thì không sao, nhưng server thật thì phải cấu hình lại.

## SQL

### Bảng
- Database chứa dữ liệu trong **bảng**. Mỗi **cột** có kiểu dữ liệu cố định, mỗi **dòng** là một bản ghi.
- Bảng `notes` tương ứng với model `Note` trong `app.py`.
```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
```
- `TEXT`: chuỗi, giống `str`.
- `NOT NULL`: bắt buộc có giá trị, giống field bắt buộc trong Pydantic.
- `SERIAL`: số nguyên tự tăng. Nó tạo bộ đếm `notes_id_seq` và đặt mặc định cho cột là `nextval(...)`, thay cho `next_id += 1`.
- `PRIMARY KEY`: mỗi dòng một giá trị khác nhau, không trùng. Nhờ nó mà tìm được đúng một dòng.
- `\d notes`: xem cấu trúc bảng.

### INSERT (giống POST)
```sql
INSERT INTO notes (title, content) VALUES ('Học SQL', 'Bài 1');
```
- Giá trị theo đúng thứ tự các cột đã liệt kê. Không ghi `id` vì `nextval` tự điền.
- Chuỗi dùng **nháy đơn** `'...'`.
- Thiếu cột `NOT NULL` thì bị từ chối **cả dòng**: `ERROR: null value in column "content" ... violates not-null constraint`. `DETAIL` cho thấy dòng bị từ chối.
- Cùng một quy tắc được kiểm tra ở 2 tầng: Pydantic (trả 422) và PostgreSQL (`NOT NULL`). Hai lớp bảo vệ.

### Id bị nhảy số
- `nextval` được gọi **trước** khi kiểm tra quy tắc. Câu `INSERT` lỗi vẫn tiêu mất một số, và bộ đếm không bao giờ trả lại số.
- Vì vậy id có lỗ hổng (1, 2, 4...) là bình thường. Xóa dòng cũng không lấp lại số.
- Giống bốc số thứ tự ở ngân hàng: bị trả về thì số đó bỏ, người sau nhận số tiếp theo.

### SELECT (giống GET)
- `SELECT * FROM notes;`: lấy tất cả các cột, tất cả các dòng.
- `SELECT * FROM notes WHERE id = 4;`: chỉ lấy những dòng thỏa điều kiện. Thay cho vòng `for` + `if` trong Python.
- SQL so sánh bằng **một dấu `=`**, không phải `==`.
- Bạn nói *muốn gì*, database tự lo *tìm thế nào*. Có `PRIMARY KEY` thì tìm theo id rất nhanh, kể cả khi có hàng triệu dòng.
- Không có dòng nào khớp thì trả về `(0 rows)`: **không phải lỗi**, là một câu trả lời hợp lệ.
- **Phân chia trách nhiệm:** database trả lời "có 0 dòng", còn code Python quyết định điều đó nghĩa là 404. Database không biết gì về HTTP.

### UPDATE (sửa)
```sql
UPDATE notes SET content = 'Bai 3 da sua' WHERE id = 4;
```
- ⚠️ **Quên `WHERE` là sửa TẤT CẢ các dòng**, không hỏi lại, không có Ctrl+Z.
- Thói quen an toàn: chạy `SELECT` với cùng `WHERE` trước để xem những dòng nào sẽ bị ảnh hưởng.
- psql in ra `UPDATE n`, với `n` là số dòng đã bị sửa (gọi là **rowcount**). `UPDATE 0` là không có dòng nào khớp. Code Python dùng số này để trả 404.

### DELETE (xóa)
```sql
DELETE FROM notes WHERE id = 2;
```
- ⚠️ `DELETE FROM notes;` mà quên `WHERE` là **xóa sạch cả bảng**. Luôn `SELECT` trước.
- Xóa dòng không tồn tại thì ra `DELETE 0`, không phải lỗi.
- `nextval` **không nhìn id lớn nhất trong bảng**, nó chỉ nhìn bộ đếm của chính nó. Xóa dòng có id lớn nhất thì note mới vẫn nhận số tiếp theo của bộ đếm.

### Tổng kết CRUD
| Việc | HTTP (FastAPI) | SQL |
|---|---|---|
| **C**reate: tạo | `POST /notes` | `INSERT` |
| **R**ead: đọc | `GET /notes/{id}` | `SELECT ... WHERE` |
| **U**pdate: sửa | *(chưa có)* | `UPDATE ... WHERE` |
| **D**elete: xóa | `DELETE /notes/{id}` | `DELETE ... WHERE` |

## Python nói chuyện với PostgreSQL

### Driver: psycopg
- Python không tự biết nói chuyện với PostgreSQL. **Driver** là người phiên dịch: gửi câu SQL đi, rồi đổi kết quả thành dữ liệu Python.
- Cài: `pip install "psycopg[binary]"`. `[binary]` là bản biên dịch sẵn, kéo theo gói `psycopg-binary`.
- `pip freeze` sắp tên gói theo chữ cái, nên gói mới có thể nằm giữa `requirements.txt`.

### Venv: tạo khác bật
- **Tạo** (`python -m venv .venv`): một lần duy nhất cho mỗi project.
- **Bật** (`source .venv/bin/activate`): mỗi lần mở terminal mới.
- Quên thì chỉ **bật** lại, đừng tạo thêm, không lại ra `.venv-1`.

### Connection string
```
postgresql://noteuser@localhost:5432/notesdb
   loại       user      máy     port    db
```
- Cùng thông tin với `psql -h localhost -U noteuser -d notesdb`, viết gọn trong một dòng.

### Kết nối và truy vấn
```python
import psycopg
from psycopg.rows import dict_row

with psycopg.connect("postgresql://noteuser@localhost:5432/notesdb", row_factory=dict_row) as conn:
    rows = conn.execute("SELECT * FROM notes").fetchall()
    note = conn.execute("SELECT * FROM notes WHERE id = %s", (4,)).fetchone()
```
- `with ... as conn`: **context manager**, tự đóng kết nối khi xong, kể cả khi bị lỗi giữa chừng.
- Mặc định mỗi dòng là một **tuple** `(1, 'Hoc SQL', 'Bai 1')`: có giá trị nhưng không có tên cột, dễ đọc nhầm cột.
- `row_factory=dict_row`: mỗi dòng là một **dict**, dùng tên cột làm key.
- `.fetchall()`: list tất cả các dòng. `.fetchone()`: một dòng, hoặc **`None`** nếu không có.
- `rows[0]["title"]`: `[0]` chọn phần tử trong list (đếm từ 0), `["title"]` chọn key trong dict. Mỗi lớp dữ liệu một cặp ngoặc vuông.
- `rows[0]` là dòng **đứng đầu** kết quả, không phải dòng có id 1. Muốn tìm theo id thì để database lọc bằng `WHERE`.
- `None` từ `.fetchone()` là lúc code Python trả 404.

### ⚠️ SQL injection
- **SAI:** `conn.execute(f"SELECT * FROM notes WHERE id = {note_id}")`. Người dùng gửi `1; DELETE FROM notes` là bảng bị xóa sạch, vì chuỗi của họ bị ghép vào và chạy như lệnh.
- **ĐÚNG:** `conn.execute("SELECT * FROM notes WHERE id = %s", (note_id,))`. Câu SQL và giá trị được gửi **riêng**, nên giá trị luôn chỉ là dữ liệu, không bao giờ bị chạy.
- Quy tắc: **không bao giờ** dùng f-string hay `+` để ghép dữ liệu người dùng vào SQL. Luôn dùng `%s`.
- `(note_id,)`: cần dấu phẩy thì Python mới hiểu đó là tuple.

### FastAPI + PostgreSQL
- Mỗi request: mở kết nối, chạy SQL, đóng lại (`with psycopg.connect(DB_URL, row_factory=dict_row) as conn:`).
- Route trả về dict từ database, còn `-> Note` / `-> list[Note]` khiến FastAPI **chuyển dict thành `Note`** (kiểm tra và lọc). Bằng chứng: thứ tự key đổi thành `title, content, id` theo đúng class.
- Không có `->` thì dữ liệu thô đi thẳng ra ngoài, không được kiểm tra.
- `INSERT ... RETURNING *`: thêm xong trả lại luôn dòng vừa tạo, kèm id do `nextval` cấp. Không cần `global next_id`.
- Nhiều `%s` được điền lần lượt theo thứ tự trong tuple: `(payload.title, payload.content)`.
- `DELETE`: đọc `.rowcount`. Bằng 0 thì `raise HTTPException(404)`.

### PUT (sửa)
- **PUT** là thay thế **toàn bộ** một resource. Client gửi đủ mọi field, nên body dùng lại `NoteCreate`.
- Id nằm trên URL (sửa note nào), body chỉ chứa nội dung mới.
- `UPDATE notes SET (title, content) = (%s, %s) WHERE id = %s RETURNING *`: gán nhiều cột cùng lúc.
- Dùng `RETURNING *` + `.fetchone()` thì không cần `rowcount`: không có dòng nào khớp thì `fetchone()` trả `None`, nên trả 404.
- **Bug đã gặp:** `(payload.title, payload.title, note_id)` nên `content` bị ghi đè bằng title. Không lỗi, vẫn 200, chỉ là lưu sai. Phải đọc **nội dung** response, không chỉ nhìn status code.

### Transaction
- PostgreSQL giữ thay đổi trong một **transaction**, chỉ lưu vĩnh viễn khi **commit**.
- Khối `with psycopg.connect(...)` tự **commit** nếu chạy hết không lỗi, tự **rollback** (hủy) nếu có lỗi giữa chừng.
- **Đã thấy tận mắt:** `DELETE` chạy xong nhưng lỗi `.rowcount()` xảy ra ngay sau, vẫn trong `with`, nên note **không bị xóa**.
- Không dùng `with` thì phải tự gọi `conn.commit()`. Quên gọi là thay đổi biến mất âm thầm.
- Giống staging trong Git: giữ tạm, commit mới lưu.

### Lỗi đã gặp
- `return Note` thay vì `return note`: trả về **class** (cái khuôn) thay vì **biến** (dữ liệu). Python phân biệt hoa thường. Quy ước: class viết hoa chữ đầu, biến viết thường.
- `.rowcount()`: `rowcount` là **thuộc tính**, không có `()`. **Hàm** (`.fetchone()`) mới gọi bằng `()`. Lỗi: `TypeError: 'int' object is not callable`.
- `HTTPException(...)` thiếu `raise`: chỉ tạo object rồi vứt đi, hàm chạy tiếp và trả 200. Phải `raise` thì mới ném lỗi ra.
- **Shadowing:** đặt biến cục bộ trùng tên biến ngoài hàm (`notes`) thì biến ngoài bị che. Không sai nhưng dễ nhầm, nên đặt tên khác.

## Cấu hình và secret

### Biến môi trường
- Cặp `TÊN=giá_trị` nằm **ngoài code**, chương trình nhận từ terminal đã khởi động nó. `$EDITOR` cũng là một biến môi trường.
- Code chỉ đọc **tên** biến, còn **giá trị** do nơi chạy cung cấp. Cùng một code, mỗi máy một cấu hình.
- `export DB_URL="..."`: tạo biến, chỉ sống trong terminal đó (giống venv). `unset DB_URL`: xóa biến.
- Python: `os.environ["DB_URL"]`. Không có thì `KeyError`. `os.environ.get("DB_URL")` thì trả `None`.

### .env và pydantic-settings
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    db_url: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Setting()
```
- Tự tìm biến `DB_URL` (không phân biệt hoa thường) và kiểm tra kiểu dữ liệu. Giống một Pydantic model, chỉ là dữ liệu đến từ cấu hình.
- **Biến môi trường thật thắng `.env`.** Server thường đặt biến trực tiếp, không cần file `.env`.
- `fastapi dev` chỉ tự tải lại khi file `.py` đổi. Sửa `.env` thì phải tắt server rồi chạy lại.
- Thiếu biến: `Field required`. Biến lạ trong `.env` (ví dụ gõ nhầm `DB_URLL`): `Extra inputs are not permitted`. Nhìn 2 lỗi cạnh nhau là thấy ngay gõ nhầm.
- **Fail fast:** cấu hình sai thì app không chịu khởi động, và nói rõ sai ở đâu. Tốt hơn nhiều so với chạy lên rồi hỏng lúc nửa đêm.

### .env và .env.example
| | `.env.example` | `.env` |
|---|---|---|
| Commit? | **Có** | **Không bao giờ** |
| Chứa | Tên biến + giá trị mẫu | Giá trị thật của máy này |
| Để làm gì | Tài liệu: cần những biến nào | App đọc khi chạy |
- Người mới clone về: `cp .env.example .env`, rồi sửa giá trị.
- Thêm biến vào `Setting` thì **luôn** thêm vào `.env.example`.
- `.gitignore` ghi `.env` thì chỉ khớp đúng tên `.env`, không chặn `.env.example`.
- **Lỗi đã gặp:** commit `.env.example` rỗng (0 byte). Kiểm tra nội dung bằng `cat` trước khi commit.

### Secret đã push là secret đã lộ
- Xóa secret khỏi code **không xóa khỏi lịch sử Git**. `git show <commit>:<file>` xem được file ở mọi thời điểm cũ.
- Lỡ push mật khẩu thật thì **đổi mật khẩu ngay** (rotate). Đừng cố xóa commit để giấu: người khác có thể đã kéo về, và bot quét GitHub có thể đã thấy.
- Vì vậy dùng `.env` ngay từ đầu, trước khi có secret thật.

### PR tự cập nhật
- Push thêm commit lên nhánh đang có PR thì **PR tự cập nhật**, không cần mở PR mới. Đây là cách sửa theo góp ý review.

## Docker

### Vì sao cần
- Đóng gói chương trình cùng mọi thứ nó cần, chạy giống hệt nhau trên mọi máy có Docker. Giải quyết câu "máy em chạy được mà".
- Mỗi dự án một container, khác phiên bản cũng không đụng nhau. Đã thấy: PostgreSQL 16.4 (container, port 5433) chạy song song PostgreSQL 18.6 (máy, port 5432).

### Image và container
| Python | Docker |
|---|---|
| `Note`: class, cái khuôn | **Image**: khuôn đóng gói sẵn, chỉ đọc |
| `note`: object tạo từ khuôn | **Container**: một bản đang chạy, tạo từ image |
- Một image tạo được nhiều container. Xóa container thì image vẫn còn.
- `docker images`: liệt kê image. `docker ps`: container **đang chạy**. `docker ps -a`: tất cả, kể cả đã dừng.

### docker run
```bash
docker run --name learn-pg -e POSTGRES_PASSWORD=secret -p 5433:5432 -v learn-pg-data:/var/lib/postgresql/data -d postgres:16.4-alpine
```
- `--name`: tên container. `-e`: biến môi trường. `-d`: chạy nền.
- `-p máy:container`: nối port. PostgreSQL trong container luôn ở 5432, trên máy truy cập qua 5433 vì 5432 đã có PostgreSQL của máy.
- `-v tên_volume:thư_mục_trong_container`: cắm volume.
- `docker run` = **tạo** + **khởi động**. Khởi động lỗi thì container vẫn được tạo và giữ tên. Phải `docker rm` rồi mới chạy lại cùng tên được.
- Port và biến môi trường **không sửa được** sau khi tạo. Muốn đổi: `docker rm -f` rồi `docker run` lại.
- `docker rm -f`: dừng rồi xóa luôn.
- `POSTGRES_PASSWORD` chỉ có tác dụng **lần đầu** khởi tạo database. Có volume cũ thì đổi biến không đổi được mật khẩu.

### Debug container
- `docker logs <tên>`: log của container, giống `journalctl`.
- `docker inspect <tên>`: toàn bộ cấu hình (biến môi trường, port, volume).
- **Lỗi đã gặp:**
  - `name ... is already in use`: container cũ bị lỗi vẫn giữ tên.
  - `password authentication failed`: gõ nhầm `sercet`. Tìm ra bằng `docker inspect`.
  - `-p 5433:5422` (sai port trong container) báo `server closed the connection unexpectedly`.
- Phân biệt: `Connection refused` là **không ai** nghe ở port đó. `server closed the connection` là **có ai đó** nhận, nhưng phía sau không có gì.

### Volume
- Dữ liệu ghi trong container sẽ mất khi container bị xóa. Container mới là bản sạch.
- **Volume** là vùng lưu trữ bên ngoài container. Xóa container thì volume vẫn còn. Giống ổ cứng rời: đổi máy, cắm ổ sang là dữ liệu còn nguyên.
- Image postgres tự tạo **anonymous volume** (tên là chuỗi số dài) nếu không có `-v`. `docker rm` không xóa nó, nên nó nằm lại mồ côi.
- **Luôn đặt tên volume.** `docker volume ls`: liệt kê. `docker volume prune -a`: dọn volume không được dùng (có hỏi xác nhận).
- Volume `docker_postgres_data` của anphat mất dữ liệu là vì ta xóa cả volume, không chỉ container.

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

