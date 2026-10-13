# youzhou-math

You Zhou 的个人数学学术主页。网站显示内容统一为英文，中文 README 仅供维护，不进入发布网站。使用 Jekyll 4.4、Markdown 和少量 CSS，内容与共用布局分开，没有数据库、JavaScript 框架或前端打包工具。

网站只包含已提供的身份、研究兴趣和联系方式，并为讲义与学术资料保留目录。尚未列出论文、报告或奖项，也没有添加讲义 PDF 或 CV 文件，不显示不存在的下载链接。实际发布状态见文末记录；本地预览成功不等于公网发布成功。

## 日常更新的完整顺序

以后每次更新，按这条顺序操作即可：**启动本地预览 → 修改 Markdown / 上传 PDF → 检查页面 → 构建与检查 → 提交推送 → 查看 Actions → 打开公开网站**。简介只需编辑对应 Markdown；上传讲义一般只涉及 `_notes/` 和 `assets/pdf/`，无需改动布局。

如果采用 GitHub 网页直接编辑，提交后会自动进入 Actions；下一次在本机编辑前，先同步远程变更，避免本机仍使用旧版本。两种编辑方式的具体步骤在后面分别说明。

## 本地预览

需要 Ruby 3.3 与 Bundler。`.ruby-version` 记录 Ruby 版本，`Gemfile` 定义依赖，`Gemfile.lock` 锁定实际版本。

macOS 若没有合适的 Ruby，可使用 Homebrew 安装：

```sh
brew install ruby@3.3
```

Apple Silicon Mac 将 Homebrew Ruby 放到当前终端的 PATH 前面：

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
```

Intel Mac 通常将该路径换成 `/usr/local/opt/ruby@3.3/bin`。确认 `ruby --version` 显示 3.3，首次安装项目依赖时运行：

```sh
cd /Users/rick/Desktop/youzhou-math
bundle config set --local path vendor/bundle
bundle install
```

上述依赖已安装且 `Gemfile` 没有变化时，不必每次重新安装。每次开启新终端，执行：

```sh
cd /Users/rick/Desktop/youzhou-math
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle exec jekyll serve --host 127.0.0.1 --baseurl ""
```

在浏览器打开 [http://127.0.0.1:4000/](http://127.0.0.1:4000/)。终端保持运行，按 `Ctrl+C` 停止。预览命令使用空 `baseurl`，以后配置了 GitHub 项目子目录，仍可从本地根路径预览。

若移动了项目文件夹，请相应调整 `cd` 的路径。使用纯文本编辑器（如 VS Code）打开项目，保存文件为 UTF-8；不要用 Word 编辑 `.md` 或 `.yml` 文件。

修改 Markdown 和 CSS 后 Jekyll 会自动重建，刷新浏览器即可。修改 `_config.yml` 后需按 `Ctrl+C` 停止服务，再执行预览命令重新启动。如果终端显示端口 4000 已占用，先停止之前的预览进程；也可以增加 `--port 4001` 并改为打开 `http://127.0.0.1:4001/`。

只构建、不启动服务器：

```sh
bundle exec jekyll build --trace
```

生成结果位于 `_site/`。`_site/`、`vendor/bundle/` 和本机 Bundler 配置均已忽略，不提交到 Git；提交 `Gemfile.lock` 以便本地与部署使用一致依赖。

构建后可使用 Python 3（仅标准库）检查导航、站内资源、锚点与 PDF 链接：

```sh
python3 scripts/check_site.py _site
```

检查脚本会从首页样式表路径识别 `baseurl`，也可以用 `--baseurl /youzhou-math` 明确指定。GitHub Actions 在上传网站前也会执行此检查；错误会中止部署。

## 文件与日常维护

| 文件 / 目录 | 用途 |
| --- | --- |
| `_config.yml` | 姓名、身份、联系方式、网址、仓库名、导航、讲义分类、CV 路径 |
| `index.md` | Home 英文简介 |
| `research.md` | Research 研究兴趣与以后确认的研究材料 |
| `notes.md` | Notes 分类目录，自动列出 `_notes/` 中的讲义 |
| `_notes/` | 每份讲义的 Markdown 页面 |
| `talks.md` | Talks，以后添加真实报告记录 |
| `cv.md` | CV 页面中的教育经历与简历说明 |
| `assets/pdf/` | 真实 PDF 文件 |
| `_layouts/`、`_includes/` | 共用页面结构、姓名区域、导航、页脚与 PDF 链接 |
| `assets/css/` | 网站样式 |
| `docs/templates/note.md` | 新讲义模板，不发布到网站 |
| `.github/workflows/pages.yml` | GitHub Actions 构建与 Pages 发布流程 |
| `scripts/check_site.py` | 构建后的导航、资源与 PDF 链接检查，不发布到网站 |

### 修改五个页面

| 想更新的内容 | 编辑位置 | 具体操作 |
| --- | --- | --- |
| Home 的英文个人介绍 | `index.md` | 修改 front matter 下的英文段落，保存后查看 Home |
| 研究兴趣与论文 | `research.md` | 修改 `Interests` 下的列表；有真实论文后更新 `Publications` |
| 讲义 | `_notes/` | 新建或编辑讲义 Markdown，目录会自动更新 |
| Notes 分类名称与说明 | `_config.yml` 的 `note_categories` | 使用英文 `title` 与 `description`，修改后重启预览 |
| 报告记录 | `talks.md` | 删除空状态说明，再写真实报告的英文题目、日期、场合与资料 |
| CV 网页正文 | `cv.md` | 更新已确认的教育或其他简历信息，下载文件另按下文配置 |

`notes.md` 主要负责自动生成目录。正常添加讲义时不需要编辑其中的 Liquid 循环。

### 修改姓名、身份和联系方式

在 `_config.yml` 中修改下列字段，显示名称和说明均保持英文：

```yaml
title: "You Zhou"
author:
  name: You Zhou
  role: Undergraduate student
  program: Mathematics and Applied Mathematics
  school: School of Mathematical Sciences
  university: Shenzhen University
  email: zhouyou2023@email.szu.edu.cn
```

`title` 控制浏览器标题中的网站名称；`author` 控制侧栏信息。只改 `author` 不会自动改写 Home 正文，因此身份变化时也检查 `index.md` 与 `cv.md`。`description` 是英文网站简介，身份或研究方向变化时一并更新。

页面顶部的两条 `---` 之间是 front matter，保存标题、布局等设置。日常编辑正文时保留这部分。例如修改 `title` 会改变页面标题，正文从第二条 `---` 后开始。

导航在 `_config.yml` 的 `navigation` 中集中维护。内部导航与讲义页面在当前标签页打开。

### 添加讲义

Notes 已准备四个分类：

| 分类 | `category` 值 |
| --- | --- |
| Evans PDE | `evans-pde` |
| Analysis | `analysis` |
| Conservation Laws | `conservation-laws` |
| Stability of Waves | `wave-stability` |

1. 复制 `docs/templates/note.md` 到 `_notes/`，例如 `_notes/evans-chapter-1.md`。
2. 将标题、摘要和正文填写为英文，设置分类、排序和 `lang: en`。
3. 如有真实 PDF，再上传 PDF 并填写 `pdf` 路径。没有 PDF 时留空。
4. 本地预览，确认 Notes 目录与讲义页面显示正确。

示例（请替换为自己的真实内容）：

```markdown
---
title: "Evans PDE: Chapter 1"
category: evans-pde
order: 10
lang: en
pdf: ""
---

Briefly describe the scope of your actual notes here.

## Contents

Write your actual mathematical notes in Markdown here.
```

以上是维护示例，先换成实际讲义内容再发布，不要把提示语当作正式材料。`layout: note` 由配置自动提供，不必逐篇添加。`order` 可省略，默认是 100；填写时使用数字，小的排在前面，建议按 10、20、30 排序，方便插入新讲义。文件名 `evans-chapter-1.md` 对应讲义网址 `/notes/evans-chapter-1/`，以后改文件名也会改网址。

分类在 `_config.yml` 的 `note_categories` 中维护。如添加新分类，其 slug 必须与讲义的 `category` 一致。集合名是 `_notes`，它负责自动生成讲义页面与目录条目，不需要手工修改导航。

### 上传和更新 PDF

将真实文件放入 `assets/pdf/`，建议使用小写英文文件名，例如 `evans-chapter-1.pdf`。然后在讲义 front matter 中填写站内绝对路径：

```yaml
pdf: "/assets/pdf/evans-chapter-1.pdf"
```

路径中不要手工加网址或 `baseurl`，模板会统一处理。更新时可直接覆盖同名 PDF；如果改名，需要同时更新相应 Markdown 或配置中的路径。大小写必须与文件名一致。

讲义页与 Notes 目录只在真实 PDF 存在时显示 PDF 链接。统一使用 `_includes/pdf-link.html` 检查 `site.static_files`，所有 PDF 在新标签页打开，并标注这一行为。正文中需要额外的 PDF 链接时也使用此 include：

```liquid
{% include pdf-link.html path="/assets/pdf/evans-chapter-1.pdf" label="PDF" %}
```

不要使用普通 Markdown 手写不存在的 PDF 下载链接。缺少文件时，include 不会输出链接；仍应确认路径正确，以免应有的链接被隐藏。

### 更新 CV

目前 `cv.md` 只写已确认的本科就读信息，`_config.yml` 中的 `cv_pdf` 为空，因此没有 CV 下载按钮。

准备好真实简历后：

1. 上传到 `assets/pdf/cv.pdf`。
2. 在 `_config.yml` 中设置 `cv_pdf: "/assets/pdf/cv.pdf"`。
3. 更新 `cv.md` 的教育经历等正文，重启预览并检查。

CV 也通过共用 include 检查文件是否存在，并在新标签页打开。删除 CV 文件或暂时不公开时，将 `cv_pdf` 恢复为空。

### 添加真实报告或论文

报告记录直接编辑 `talks.md`。有真实资料后，删除 `No talks are listed here yet.` 及后续空状态说明，按下列模式填入实际内容：

```markdown
## Actual talk title

- Date: YYYY-MM-DD
- Venue: Actual seminar or conference name

An English description of the actual talk.

{% include pdf-link.html path="/assets/pdf/actual-talk-slides.pdf" label="Slides (PDF)" %}
```

`YYYY-MM-DD`、题目、场合、介绍和文件名均须替换。没有幻灯片时删除 include 行，不创建空 PDF。多个报告按日期从新到旧排列即可。

论文记录写在 `research.md` 的 `Publications` 下，用真实的作者、标题、期刊或准确状态、年份和 DOI / arXiv 链接替换空状态说明。例如使用这种结构，不要直接发布占位文字：

```markdown
- Actual authors. *Actual paper title*. Actual journal or accurate status, actual year.
  [DOI or arXiv](https://the-actual-source-url)
```

只有确实存在的材料才列出。尚未发表的材料明确写其真实状态，例如 `Preprint`；不要将学习计划写成论文或已完成报告。若另外提供论文 PDF，仍使用共用 PDF include，并先上传实际文件。

## 修改网站地址与仓库名

这些设置只需在 `_config.yml` 中集中修改。当前选择使用 GitHub 账号 `youzhouu` 的项目站点，配置为：

```yaml
url: "https://youzhouu.github.io"
baseurl: "/youzhou-math"
repository: "youzhouu/youzhou-math"
```

`url` 只写域名与协议、不带末尾 `/`；`baseurl` 写项目子目录，带开头 `/`、不带末尾 `/`；`repository` 写 GitHub 的 `用户名/仓库名`，不写完整 URL。

对应的目标公开地址是 `https://youzhouu.github.io/youzhou-math/`。这是本轮已选定的地址，实际部署成功情况见文末记录。

| 发布位置 | `url` | `baseurl` | `repository` |
| --- | --- | --- | --- |
| 项目仓库 `youzhou-math` | `https://USERNAME.github.io` | `/youzhou-math` | `USERNAME/youzhou-math` |
| 用户主页仓库 `USERNAME.github.io` | `https://USERNAME.github.io` | `""` | `USERNAME/USERNAME.github.io` |
| 自定义域名 | `https://example.org` | `""` | 真实的 `用户名/仓库名` |

表中的 `USERNAME` 与 `example.org` 都是说明用占位内容，正式发布前替换为真实值。模板中的站内资源与导航使用 `relative_url`，因此修改 `baseurl` 后不必逐个替换链接。自己在 Markdown 中添加站内页面链接时也采用：

```liquid
[Research]({{ '/research/' | relative_url }})
```

改仓库名或 GitHub 用户名后，重新核对这三个字段。`repository` 是集中保存的仓库标识，不会自动创建、改名或连接远程仓库。

### `youzhou-math.github.io` 的域名规则

**可以采用这个地址，但账号或组织名必须是 `youzhou-math`，并且网站仓库必须是该账号下的 `youzhou-math.github.io`。** GitHub 的个人 / 组织根站默认域名匹配所有者名称；只在其他用户名下创建一个叫 `youzhou-math.github.io` 的仓库，不能取得这个子域。[GitHub Pages 网站类型说明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

若使用该账号与仓库，配置为：

```yaml
url: "https://youzhou-math.github.io"
baseurl: ""
repository: "youzhou-math/youzhou-math.github.io"
```

当前文件夹仍可保留 `youzhou-math`，文件夹名不决定域名。本轮使用现有账号 `youzhouu`，因此选择项目地址 `https://youzhouu.github.io/youzhou-math/`。`github.io` 子域由 GitHub 分配，不能作为独立自定义域名任意申请；独立域名需另外购买并设置 DNS。

是否能注册 `youzhou-math` 账号或组织名，需要 GitHub 实际注册或创建时确认；本 README 不将它标为已取得的域名，也不将它标为已上线地址。

## 首次公开发布

本项目选择 **GitHub Actions 构建 Jekyll，再将 `_site/` 发布到 GitHub Pages**。Actions 使用 Ruby 3.3 与项目的 Gemfile，运行 `bundle exec jekyll build --trace`；不依赖 GitHub Pages 分支模式自带的 Jekyll 版本，也无需手工提交生成文件或创建 `gh-pages` 分支。此方式支持使用本项目锁定的 Jekyll 4.4。[Jekyll 官方说明](https://jekyllrb.com/docs/continuous-integration/github-actions/)

发布需要登录 GitHub、拥有目标仓库的管理权限，并确认使用哪个个人账号或组织。使用 GitHub Free 时，网站源码仓库须设为 **Public**；网站内容会公开访问。[GitHub 创建 Pages 网站说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

首次发布的步骤如下；若文末已记录仓库和部署结果，不必重新创建仓库：

1. 确定 GitHub 用户名、仓库名和网址，填写 `_config.yml` 的 `url`、`baseurl`、`repository`。
2. 登录 GitHub，创建对应的 **Public** 仓库。若准备从这个本地项目推送，创建时不要额外初始化 README、`.gitignore` 或 License，避免与本地已有文件形成两个独立历史。[GitHub 本地项目上传说明](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
3. 按下面的“本地 Git 首次设置与推送”提交源码和 `Gemfile.lock` 到 `main`。如果使用其他发布分支，修改工作流中的 `on.push.branches`。
4. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。[GitHub 发布来源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
5. 在 **Actions** 中选择 **Build and deploy Jekyll to GitHub Pages → Run workflow → main → Run workflow**；启用之后，每次推送到 `main` 也会自动触发。
6. 确认 `build`、`deploy` 都成功，再从 **Settings → Pages → Visit site** 或部署结果打开实际网址，检查 Home、Research、Notes、Talks、CV 和实际 PDF。

工作流用 `configure-pages` 配置部署上下文、`upload-pages-artifact` 上传 `_site/`、`deploy-pages` 发布到 `github-pages` 环境。使用 GitHub 自动提供的 `GITHUB_TOKEN` 与所需的 Pages / OIDC 权限，无需个人访问令牌。[GitHub 自定义工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

生产构建直接读取 `_config.yml` 的 `url` 和 `baseurl`，工作流不会覆盖它们。上传前务必确认这些值对应实际 Pages 地址，否则项目子目录中的 CSS、导航或 PDF 路径可能不正确。自定义域名的 DNS 与 Pages 域名设置留到选定域名后处理。

发布前可模拟项目子目录预览：

```sh
bundle exec jekyll serve --host 127.0.0.1 --baseurl /youzhou-math
```

打开 [http://127.0.0.1:4000/youzhou-math/](http://127.0.0.1:4000/youzhou-math/)，检查导航、CSS 与 PDF。手机可在浏览器响应式模式查看；第一版采用窄屏上下排列，无头像、横幅或动画。

### 本地 Git 首次设置与推送

本地仓库初始化、创建提交、连接远程仓库、推送上线是四件不同的事，不要由“已有 `.git/`”推断已完成后三步。先在项目目录检查：

```sh
git status
git log --oneline -5
git remote -v
git config --get user.name
git config --get user.email
```

`git log` 提示尚无提交时，说明还需要首次提交；`git remote -v` 没有输出时，说明还没有远程地址。姓名或邮箱为空时，先选择你希望用于 Git 提交的真实姓名和邮箱，也可以使用 GitHub **Settings → Emails** 提供的 noreply 邮箱。以下邮箱是占位符，先替换再执行；`--local` 只设置本项目：

```sh
git config --local user.name "You Zhou"
git config --local user.email "YOUR_VERIFIED_OR_NOREPLY_EMAIL"
```

构建和检查通过后，创建首次提交：

```sh
git add .
git diff --cached --stat
git commit -m "Create academic homepage"
```

查看暂存列表，确认包含网站源码、工作流、检查脚本、README 和 `Gemfile.lock`，不包含 `_site/` 或 `vendor/`。若原来已有提交，直接使用后面的日常提交流程。

从 GitHub 仓库 **Code → HTTPS** 复制真实远程 URL。下面的 `ACTUAL-REMOTE-URL` 必须替换为复制的 URL；只有尚无 `origin` 时才执行 `remote add`：

```sh
git remote add origin ACTUAL-REMOTE-URL
git remote -v
git push -u origin main
```

已经有 `origin` 时先核对它，地址正确则直接推送，不重复添加。若需要更换地址，使用 `git remote set-url origin ACTUAL-REMOTE-URL`。

本机推送还需要 GitHub 身份验证。可使用 GitHub CLI 的 `gh auth login` 按浏览器流程登录，或使用已配置的 SSH / 凭据管理器；GitHub 网页的登录密码不能直接用作 HTTPS `git push` 的密码。工作流自身的 `GITHUB_TOKEN` 不等于本机推送凭据。[GitHub 身份验证说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)

## 发布后的日常操作

### 在 GitHub 网页修改简介

适合改几个段落或联系方式，不需要在本机安装依赖：

1. 登录 GitHub，打开实际网站仓库，确认当前分支是 `main`。
2. 打开要修改的文件，例如 `index.md`，点击铅笔按钮 **Edit this file**。
3. 修改英文正文，保留顶部 front matter。编辑 `_config.yml` 时保持缩进，用空格而不是 Tab。
4. 点击 **Preview** 查看 Markdown，再点击 **Commit changes…**，写清更新内容。
5. 若允许直接提交，选择提交到 `main`；若要求新分支，选择新分支、创建 Pull Request，合并到 `main` 后才触发网站发布。
6. 到 **Actions** 确认新的 `build` 与 `deploy` 成功，再打开公开网页。

GitHub 的 Markdown Preview 不执行 Jekyll / Liquid，因此它不是最终网页预览；include 或目录循环需等待网站构建后查看。受保护的 `main` 可能要求通过 Pull Request 合并。[GitHub 文件编辑说明](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)

### 在 GitHub 网页添加讲义与上传 PDF

1. 打开仓库的 `_notes/` 目录，选择 **Add file → Create new file**。
2. 文件名写 `actual-note-name.md`，复制上面的英文讲义格式并填写真实内容，然后提交到 `main` 或通过 Pull Request 合并。
3. 如果有 PDF，进入 `assets/pdf/`，选择 **Add file → Upload files**，拖入真实文件并提交。
4. 回到对应讲义 Markdown，把 `pdf` 填为 `/assets/pdf/实际文件名.pdf`。英文文件名与大小写须完全匹配。
5. 等待 Actions 成功，检查 Notes 目录与讲义页中的 PDF 链接。

先上传 PDF、后填写路径，可以避免先显示路径却没有文件的维护状态；本项目在文件缺少时会自动隐藏链接。GitHub 网页单文件上传限制为 25 MiB，若 PDF 更大，可先压缩 PDF 或使用本地 Git 上传。[GitHub 上传文件说明](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

网页上传新 CV 的操作相同：上传 `assets/pdf/cv.pdf` 后，再编辑 `_config.yml` 的 `cv_pdf`。更新同名文件时核对提交结果，确认覆盖的是期望的文件，最后实际打开 PDF 查看内容。

### 在本机编辑、检查、提交和推送

首次设置与远程连接已经完成后，日常从项目目录开始。若之前在 GitHub 网页改过文件，且本地没有未提交修改，先同步：

```sh
git status
git pull --ff-only origin main
```

若 `git status` 显示未提交修改，先保存、提交或处理这些修改再同步。`pull --ff-only` 失败时说明需要处理分支差异，不要用强制推送覆盖网页上的更新。

启动预览并编辑，保存后检查五个导航页、相关讲义与 PDF。完成后停止预览，运行：

```sh
bundle exec jekyll build --trace
python3 scripts/check_site.py _site
git diff --check
git diff
git status
```

构建必须成功，检查脚本必须输出 `PASS`，再提交。本地检查脚本验证站内导航、文件、锚点、PDF 标签页行为及维护文件排除；它不联网验证外部 DOI / arXiv 链接，也不代替浏览器查看排版。

只把本次修改的文件加入提交。例如添加一份真实讲义和 PDF 时：

```sh
git add _notes/actual-note-name.md assets/pdf/actual-note-name.pdf
git diff --cached --stat
git commit -m "Add study notes"
git push origin main
```

将示例文件名换成实际文件名；若没有 PDF，去掉 PDF 路径。修改简介时改为 `git add index.md`；修改 CV 时按实际变更加入 `cv.md`、`_config.yml` 和对应 PDF。多个相关文件最好放在同一个提交中，便于追踪与回滚。

### 查看发布结果与处理失败

1. 打开仓库 **Actions**，在左侧选择 **Build and deploy Jekyll to GitHub Pages**。
2. 点击最新运行，核对它对应的提交信息与提交编号，确认是刚才的修改。
3. `build` 和 `deploy` 都为绿色成功，才表示这次内容已经完成构建与部署。黄色表示仍在等待或运行，红色表示失败。
4. 若失败，打开红色 job 并展开失败步骤，阅读日志。`Build website` 常见错误是 YAML 缩进、front matter 或 Liquid 写法；`Check navigation and local links` 会指出缺失资源和错误路径；`Configure GitHub Pages` / `deploy` 失败时检查 **Settings → Pages** 来源和仓库权限。
5. 修正文件并再次提交，新的运行会自动启动。只有临时网络等问题、文件无需修改时，才尝试 **Re-run failed jobs**。

Actions 日志记录每个 job 和步骤的状态，可据此定位错误。[GitHub 查看工作流历史说明](https://docs.github.com/en/actions/how-tos/monitor-workflows/view-workflow-run-history)

部署成功后，从 **Settings → Pages → Visit site** 或该次部署 URL 打开网页。GitHub 官方说明，推送后的公开更新可能需要最多约 10 分钟；如果看到旧页面，先核对成功运行的提交编号，再强制刷新（Mac 浏览器通常 `Command+Shift+R`），或使用无痕窗口。[GitHub Pages 发布说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

如果同名 PDF 仍显示旧内容，关闭旧 PDF 标签页并重新打开链接，也可临时在地址后加 `?v=本次日期` 检查，例如 `cv.pdf?v=20261013`。仍无更新时检查仓库中的文件是否确实更新，不必先清除 Ruby 的 Bundler 缓存；依赖缓存与浏览器页面缓存是不同的东西。

### 回滚错误更新

没有提交的改动，可在编辑器中撤销，或用已有备份恢复。若已有提交历史，而且只想放弃 `index.md` 的本次未提交修改，先备份需要保留的内容，再执行：

```sh
git restore --source=HEAD --staged --worktree -- index.md
```

这会把该文件的暂存与工作区内容恢复到最近一次提交，覆盖该文件未提交的修改；没有首次提交时不能使用 `HEAD` 恢复。[Git restore 文档](https://git-scm.com/docs/git-restore)

已推送或已发布的错误修改，用新的恢复提交回滚。先保存其他本地修改、同步 `main`，运行 `git log --oneline -10` 找到错误提交编号，然后执行以下步骤；把 `BAD-COMMIT-SHA` 替换成实际编号：

```sh
git revert --no-edit BAD-COMMIT-SHA
bundle exec jekyll build --trace
python3 scripts/check_site.py _site
git push origin main
```

`git revert` 生成一个反向修改的新提交，保留历史，推送后会再次部署。[Git revert 文档](https://git-scm.com/docs/git-revert)

网页编辑的小错误，也可以从该文件 **History** 查看正确的旧内容，再用铅笔编辑恢复并创建新提交。若通过 Pull Request 发布，可以在已合并 Pull Request 中使用 **Revert** 创建恢复 Pull Request，合并到 `main` 后生效。恢复后仍需检查 Actions 和公开网页。[GitHub 恢复 Pull Request 说明](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request)

## 待补充的真实资料

- GitHub Pages 实际部署结果与公开网址访问验证（当前已选 `youzhouu/youzhou-math` 项目站点）。
- Evans PDE、分析、守恒律、波的稳定性讲义正文与实际 PDF。
- 完整 CV 与可公开的简历 PDF。
- 若有真实研究成果或论文，补充准确标题、作者、状态和链接。
- 若有真实学术报告，补充日期、题目、场合和可公开材料。
- 若需要展示奖项、项目、教育起止时间或导师信息，先确认事实再添加。
- 头像暂时留空；以后确定照片与展示意愿后再添加。

不要以示例条目或空下载文件替代真实学术材料。日常维护主要是修改 Markdown、上传 PDF，通常无需改动布局或 CSS。

## 第一版验证记录（2026-10-13）

- Ruby 3.3.12、Jekyll 4.4.1 本地构建成功；依赖已写入 `Gemfile.lock`。
- 根路径与 `/youzhou-math` 子路径的 6 个页面通过导航、资源和锚点检查。
- 在项目以外的临时副本中验证中文讲义、存在的 PDF/CV 与不存在的 PDF；真实项目没有测试讲义或测试 PDF。
- 实际浏览器检查 1280 像素桌面双栏及 375、320 像素手机布局，没有横向溢出；已查看五个导航页面。
- GitHub Actions 工作流 YAML 已检查，尚未连接 GitHub 或实际执行 Pages 部署。
- 首轮 `jekyll doctor` 对当时为空的 `url` 给出提醒；后续已按选定项目地址填写 `_config.yml`。

第一版时，本地 Git 已初始化为 `main` 分支；当时未设置 Git 提交姓名和邮箱，尚未创建提交或连接远程仓库。

## 全英文修改与发布记录（2026-10-13）

- 网站名称使用 `You Zhou`；页面正文、导航、姓名区域和讲义模板统一使用英文。
- 中文 README、维护脚本与模板目录不发布到网站。
- 已确认使用现有 GitHub 账号 `youzhouu` 的项目站点，集中配置已改为 `youzhouu/youzhou-math`。
- 目标公开地址：`https://youzhouu.github.io/youzhou-math/`。
- `youzhou-math.github.io` 需要同名个人或组织账号；本轮没有修改 GitHub 用户名。
- 用户已授权公开发布，目前发布操作进行中；尚未在此记录成功的 Pages 部署结果。公开地址是否可访问以实际 Actions `deploy` 成功及网页验证为准。
