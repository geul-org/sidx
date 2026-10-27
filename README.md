# SIDX

자주 쓰이는 위키데이터 Q아이디와 GEUL ID를 분석해, 의미가 가까울수록 번호도 가깝게 SIDX를 배정하는 프로젝트다.

| 항목 | 값 |
|---|---|
| 저장소 | [geul-org/sidx](https://github.com/geul-org/sidx) (옛 이름 geul-entity) |
| 명세 | GEUL v1 Reference `GEUL-SIDX`(Codec `0011`) |
| 상태 | 재출발. 배정 결과는 아직 없다 |

## SIDX

SIDX(Semantic-aligned Index)는 의미 주소다. 번호가 가까우면 의미도 가깝다.

- GEUL ID(Reference `GEUL`, `0010`)와 역할이 다르다. GEUL ID는 대체로 순서대로 배정하는 정체성 ID이고 번호에 의미가 없다. SIDX는 의미가 가까운 대상에 가까운 값을 준다(GEUL v1 GEUL-SIDX 배정 방침).
- 위키데이터 Q아이디(`WIKIDATA-QID`, `0100`)도 번호에 의미가 없다.
- 한 대상이 GEUL ID와 SIDX를 함께 가지면 두 Reference를 `SAME-NODE`로 잇는다.

## 왜

GEUL 레코드는 색인으로 쓴다. 색인 번호가 의미 순서를 따르면 다음이 쉬워진다.

- 범위 질의. 의미가 가까운 대상이 한 정수 구간에 모이면 "이 근처"를 구간 하나로 찾는다.
- 정렬·압축. 정렬한 색인에서 이웃 값의 차가 작아진다.
- 근사 비교. 번호만 보고 같은 동네인지 먼저 거른다.

한계도 있다. 의미는 여러 축이지만 번호는 한 줄이다. 가까운 번호는 가까운 의미를 뜻하도록 배정하지만, 먼 번호가 먼 의미라는 보장은 없다.

## 입력

| 입력 | 원천 | 상태 |
|---|---|---|
| Q아이디 사용 빈도 | 위키데이터. geuldev 스키마 `wikidata`([wikipg](https://github.com/geul-org/wikipg) 적재) | 새 적재본으로 아직 집계하지 않았다. `artifacts/wikidata/`의 집계는 옛 적재본 기준이다 |
| Q아이디 사이 관계 | 같은 DB의 `P31`(instance of), `P279`(subclass of) 등 | `artifacts/wikidata/wikitrees1.json`(옛 적재본) |
| GEUL ID 사용 빈도 | GEUL 문서에 나오는 Reference | GEUL ID 배정 규칙과 레지스트리가 GEUL v1에서 미결정이다 |

- CC0 원천만 쓴다. 위키데이터는 CC0다.
- WordNet, 표준국어대사전 등 CC0가 아닌 자료는 배정 근거로 쓰지 않고, 그 내용·구조·목록을 배정 결과에 넣지 않는다.

## 배정 (초안)

1. 대상을 고른다. 사용 빈도 상위부터 한다. 통계가 모이기 전의 대상은 GEUL ID로 가리킨다(GEUL v1 배정 방침).
2. 근접도를 잰다. 후보는 위키데이터 계층(`P31`·`P279`) 거리, 속성·값 공유, GEUL 문서 안 공동 출현이다. 아직 정하지 않았다.
3. 한 줄로 놓는다. 가까운 대상끼리 이웃하도록 정렬한다(예: 계층 트리 순회, 군집 뒤 순서화).
4. 번호를 준다. 이웃 사이에 빈자리를 남기는 희소 배정으로 한다. 이미 준 번호는 옮기지 않는다(append-only).
5. 공표한다. 배정을 GEUL 문서로 내고, 같은 대상의 GEUL-SIDX와 GEUL·WIKIDATA-QID를 `SAME-NODE`로 잇는다.

## GEUL v1과의 관계

GEUL-SIDX는 선언 Reference다.

```
TAG WORD          0000 0LLL L001 1QQQ      CCCC = 0011
[Length 확장 TAG]
SIDX              나머지 전부
```

- 양화는 Quantifier `QQQ`로만 한다. SIDX 값에 양화를 넣지 않는다.
- 폭은 미결정이다. 4 WORD(64비트)와 16 WORD 등을 검토 중이다. 상위 비트에 의미가 있어 다른 선언 Codec의 "가장 짧은 폭" 규칙을 그대로 쓸 수 없으므로 고정 폭(또는 하위 형식별 고정 폭)이 될 것이다. 정해질 때까지 규격 문서는 SIDX를 나머지 폭 날값으로 선언한다.
- 비규범 예시: 64비트 `0x1234 5678 9abc def0`, Identified → `0218 1234 5678 9abc def0`.
- 정수값이 같으면 같은 대상이다. 배정으로 유일성을 보장한다.
- 명세: geul-dev `docs/reference/GEUL-SIDX.md`, 공개 문법 [geul.org/ko/grammar/reference](https://geul.org/ko/grammar/reference/).
- geul.org 용어 정의 문서 `sidx`(`0x0001000000000003`)가 이 저장소를 도구로 가리킨다(geul-dev `docs/GEUL-ORG.md`). 옛 0908 판 위키데이터 적재 도구로 커밋 `4225b3b`의 `artifacts/wikidata/postgres.go`가 인용된다(gogeulwiki README). 그래서 이 파일은 경로를 옮기지 않는다.

## 저장소 구성

```
README.md
artifacts/
  wikidata/    위키데이터 집계 데이터와 도구 (옛 적재본 기준)
  scripts/     옛 48비트 Entity SIDX 파이프라인 (자료로만 둔다)
files/
  legacy/      옛 설계 문서와 산출물
specs/         비어 있다
```

### artifacts/wikidata

| 파일 | 내용 |
|---|---|
| `postgres.go` | 위키데이터 JSON 덤프를 옛 `geuldev.public` 표에 적재하던 도구. 그 표는 2026-10-26 삭제됐고 wikipg가 대신한다 |
| `wikidata.sql` | 옛 적재 표 정의(`entities`, `triples`, `hierarchy` 등) |
| `property_usage.sql` | 속성 사용량·속성-목적어 빈도 표 정의(`property_usage_stats`, `property_object_stats`) |
| `query.go` | SELECT 결과를 JSON 파일로 저장한다 |
| `instance_top1000.json` | `P31` 목적어 빈도 상위 1,000 |
| `usage_top1000.json` | 속성-목적어 쌍 빈도 상위 1,000 |
| `tops.json` | `P31` 목적어 `[QID, 레이블, 개체 수]` 455개. 위키미디어 범주(`Q4167836`)는 없다 |
| `country.json` | `P17`(country) 목적어 빈도 4,393개 |
| `language.json` | `P407`(language of work or name) 목적어 빈도 2,822개 |
| `wikitrees1.py`, `wikitrees1.json` | `P31` 목적어 타입의 `P279` 계층. 타입 108,790, 간선 122,551, 루트 1,555, 잎 65,331, 다중 부모 26,525 |
| `exec.py`, `topcandidate.py` | `wikitrees1.json` 조회. 경로가 `geulso/wikidata/`로 박혀 있다 |

- DB 도구는 옛 표를 전제하고 접속 문자열이 코드에 박혀 있다. `geuldev.wikidata` 기준으로 고쳐 다시 집계해야 한다.

### artifacts/scripts

옛 64비트 Entity SIDX(Prefix·Mode·EntityType·48비트 속성) 인코더와 5단계 파이프라인(`stage1_extract.py`~`stage5_validate.py`)이다. 옛 표와 `geulwork` DB, `references/*.json`(지금 `files/legacy/references/`)을 전제하므로 그대로는 돌지 않는다.

### files/legacy

옛 Entity Node 설계(SIDX v0.11, Entity Node v0.4, 인코더 명세, 64개 EntityType 48비트 스키마, 코드북, 단계 보고서, 계획)다. GEUL v1에서 폐기된 설계다. 그 안의 수치(커버리지, 충돌률 등)는 다시 검증하지 않았다.

- 폐기 사유: GEUL v1은 레코드 종류를 TAG WORD로 가르고 양화를 `QQQ`로 한다. 옛 설계의 Prefix·Mode가 설 자리가 없다. 같은 SIDX에 여러 개체를 허용하던 옛 성질(Non-unique)은 "정수값이 같으면 같은 대상"과 맞지 않는다.
- 가져갈 것: 빈도·계층 집계 방법, 위키미디어 내부 항목 제외 목록(`files/legacy/references/uncovered_types_analysis.md`), `P279` 상향 탐색 구상(`files/legacy/docs/entity-sidx-다음단계.md`, 미구현).

## DB 접속 설정

스크립트는 DB 비밀번호를 저장소 루트의 `.env`에서 읽는다(git 제외). `.env.example`을 `.env`로 복사하고 값을 채운다.

```
GEUL_READER_PASSWORD=   # geul_reader (geuldev 읽기)
GEUL_WRITER_PASSWORD=   # geul_writer (geulwork 쓰기)
POSTGRES_PASSWORD=      # postgres (artifacts/wikidata의 적재·조회 도구)
```

- Python은 `artifacts/scripts/sidx_env.py`의 `env()`, Go(`artifacts/wikidata/*.go`)는 파일 안의 `envValue()`로 읽는다. 환경변수에 같은 이름이 있으면 그 값이 우선이다.

## 라이선스

- 배정 결과(SIDX 표, GEUL 문서)는 CC0로 공표한다.
- 코드는 MIT다. LICENSE 파일은 아직 두지 않았다.

## 열린 질문

- **폭.** 4 WORD, 16 WORD 등 무엇으로 할지. 고정 폭이라도 판본이 폭을 선언하고 늘릴 수 있게 둘지.
- **근접도.** 무엇으로 잴지(계층 거리, 속성 공유, 공동 출현). 결정적이고 재현 가능해야 한다.
- **비트 구획.** 명세는 SIDX를 "비트에 의미(종류, 속성)를 담은 식별자"라고도 한다. 상위 비트에 종류 구획을 둘지, 순서만 볼지.
- **추가 시 안정성.** 빈자리를 얼마나 남길지, 빈자리가 차면 어떻게 할지. 번호를 옮겨야 하면 SIDX를 영구 식별자가 아니라 레지스트리 판본에 묶인 색인으로 볼지(명세 미결정).
- **판본과 공표.** 배정을 어떤 GEUL 문서(Issuer, 문서 ID)로 내고 판본을 어떻게 매길지. 명세도 "코드북과 레지스트리 공개 형식"을 미결정으로 둔다.
- **빈도 기준.** "자주 쓰이는"을 위키데이터 안 사용 빈도로 볼지, GEUL 문서 안 등장 빈도로 볼지. 어디서 자를지.
- **대상 식별.** GEUL ID 레지스트리가 미정이다. 한 대상이 Q아이디와 GEUL ID를 둘 다 가지면 SIDX 하나만 받는다고 볼지.
- **다중 이웃.** 부모가 여럿인 대상(`P279` 다중 부모 26,525)은 한 줄에서 한 자리만 받는다. 어느 이웃 곁에 둘지.

## 관련 저장소

| 저장소 | 관계 |
|---|---|
| geul-dev | GEUL v1 명세 |
| [wikipg](https://github.com/geul-org/wikipg) | 위키데이터 덤프 → geuldev `wikidata` 적재 |
| [gogeulwiki](https://github.com/geul-org/gogeulwiki) | 위키데이터 → GEUL 변환 |
| [gogeul](https://github.com/geul-org/gogeul) | GEUL Go 라이브러리 |
