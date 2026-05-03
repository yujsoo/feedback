import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import os

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "1500384327941230604"))
KST = pytz.timezone("Asia/Seoul")
START_TUESDAY = datetime(2026, 5, 6, tzinfo=KST)
START_FRIDAY = datetime(2026, 5, 9, tzinfo=KST)

TUESDAY_PROBLEMS = {
    1:  ("React",               "useState vs useRef — 언제 무엇을 쓸까?",
         "아래 두 가지를 각각 구현해보세요.\n\n**① 숫자 카운터**\n버튼 클릭 시 숫자가 화면에 표시되며 증가 → `useState` 사용\n\n**② 렌더링 없는 카운터**\n버튼 클릭 시 콘솔에만 찍히고 화면은 리렌더링 안 됨 → `useRef` 사용\n\n```jsx\nimport { useState, useRef } from 'react';\nexport default function App() {\n  // ① useState 카운터 구현\n  // ② useRef 카운터 구현\n}\n```\n\n💬 useState와 useRef의 차이를 한 줄로 설명해보세요!"),
    2:  ("Vue 3",               "ref / reactive / computed 차이 알기",
         "아래 세 가지를 각각 사용하는 예시를 구현해보세요.\n\n**① ref** — 단순 숫자 카운터\n**② reactive** — 이름 + 나이가 담긴 객체 상태 관리\n**③ computed** — 이름과 나이를 조합한 소개 문장 자동 생성\n\n```vue\n<script setup>\nimport { ref, reactive, computed } from 'vue';\n</script>\n```\n\n💬 ref와 reactive 중 언제 무엇을 쓰는 게 좋을까요?"),
    3:  ("React",               "useEffect & 라이프사이클 이해하기",
         "아래 세 가지 케이스를 useEffect로 구현해보세요.\n\n**① 마운트 시 한 번만 실행** — 진입 시 콘솔에 'Hello!' 출력\n**② 특정 값이 바뀔 때 실행** — input 값 바뀔 때마다 콘솔 출력\n**③ 언마운트 시 정리** — setInterval 시작 후 clearInterval"),
    4:  ("Vue 3",               "watch / watchEffect 차이 알기",
         "아래 두 가지를 구현하며 차이를 느껴보세요.\n\n**① watch** — 검색어 input이 바뀔 때만 콘솔 출력\n**② watchEffect** — 페이지 진입 즉시 실행 + 자동 추적\n\n💬 watch와 watchEffect의 가장 큰 차이점은?"),
    5:  ("Next.js",             "App Router — SSR / CSR / SSG 차이",
         "Next.js App Router 기준으로 세 가지를 각각 구현해보세요.\n\n**① SSG** — 빌드 시 데이터를 미리 가져오는 정적 페이지\n**② SSR** — 요청 시마다 서버에서 데이터 가져오기\n**③ CSR** — 클라이언트에서 useEffect로 데이터 가져오기\n\n```tsx\nfetch(url, { cache: 'force-cache' })  // SSG\nfetch(url, { cache: 'no-store' })     // SSR\n```"),
    6:  ("React",               "커스텀 훅 만들기",
         "**useLocalStorage** 훅을 만들어보세요.\n- localStorage에 값을 저장/불러오기\n- 새로고침해도 값이 유지됨\n\n```jsx\nfunction useLocalStorage(key, initialValue) {\n  // 여기에 구현\n}\nconst [name, setName] = useLocalStorage('name', '');\n```"),
    7:  ("Nuxt 3",              "useFetch / 라우팅 / 레이아웃",
         "Nuxt 3에서 아래 세 가지를 구현해보세요.\n\n**① useFetch** — JSONPlaceholder API에서 할 일 목록 가져오기\n**② 라우팅** — /todos 와 /todos/[id] 페이지\n**③ 레이아웃** — 모든 페이지에 공통 헤더 적용"),
    8:  ("React",               "Context API로 전역 상태 관리",
         "Context API로 다크모드 기능을 구현해보세요.\n\n**① ThemeContext 생성** — 'light' / 'dark' 상태\n**② Provider로 감싸기**\n**③ 어떤 컴포넌트에서든 토글 가능**"),
    9:  ("Vue 3 + Pinia",       "Pinia로 장바구니 구현",
         "Pinia store를 만들어 장바구니 기능을 구현해보세요.\n\n**① store** — 상품 목록, 장바구니, 총 금액(computed)\n**② 액션** — 상품 추가 / 삭제\n**③ 컴포넌트** — 상품 목록 + 장바구니 페이지"),
    10: ("React + Zustand",     "Zustand로 장바구니 구현",
         "Zustand store를 만들어 장바구니 기능을 구현해보세요.\n\n```js\nconst useCartStore = create((set) => ({\n  items: [],\n  addItem: (item) => set((state) => ({ items: [...state.items, item] })),\n  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) }))\n}))\n```\n\n💬 Context API와 비교했을 때 Zustand의 장점은?"),
    11: ("Next.js",             "동적 라우팅 & 미들웨어",
         "**① /blog/[slug]** — 동적 라우팅 + generateStaticParams\n**② 미들웨어** — /dashboard 접근 시 비로그인이면 /login 리다이렉트"),
    12: ("Nuxt 3",              "비동기 처리 & 에러 핸들링",
         "**① useAsyncData** — 로딩/에러 상태 표시\n**② error.vue** — 전역 에러 페이지\n**③ try/catch** — API 실패 시 메시지 표시"),
    13: ("Next.js",             "React Server Components 이해하기",
         "**① Server Component** — async/await로 데이터 직접 fetch\n**② Client Component** — 'use client' + useState\n**③ 혼합 사용** — Server 안에 Client 포함\n\n💬 어떤 컴포넌트를 Server / Client로 나눠야 할까요?"),
    14: ("Vue 3",               "Composables 패턴으로 로직 분리",
         "**① useMouse** — 마우스 위치(x, y) 반환\n**② useFetch** — 데이터, 로딩, 에러 상태 반환\n**③ 하나의 컴포넌트에서 두 composable 함께 사용**"),
    15: ("React + TypeScript",  "TypeScript + React 기초",
         "**① Props 타입** — interface로 선언\n**② useState 타입** — 제네릭 사용\n**③ 이벤트 타입** — React.ChangeEvent, React.MouseEvent\n\n```tsx\ninterface CardProps { title: string; onClick: () => void; }\nconst [isLiked, setIsLiked] = useState<boolean>(false);\n```"),
    16: ("Vue 3 + TypeScript",  "TypeScript + Vue 3",
         "**① defineProps 타입** — withDefaults 사용\n**② ref 타입** — Ref<타입> 명시\n**③ defineEmits 타입** 정의\n\n```vue\n<script setup lang=\"ts\">\nconst props = withDefaults(defineProps<{ title: string; count?: number }>(), { count: 0 });\n</script>\n```"),
    17: ("React + TanStack Query", "TanStack Query로 서버 상태 관리",
         "**① useQuery** — 게시글 목록 (로딩/에러/성공 상태)\n**② useMutation** — 새 게시글 추가 후 목록 자동 갱신\n**③ 캐싱 확인** — 네트워크 탭에서 직접 확인"),
    18: ("Vue 3 + VueUse",      "VueUse로 생산성 높이기",
         "**① useLocalStorage** — 다크모드 자동 저장\n**② useIntersectionObserver** — 화면에 보일 때 애니메이션\n**③ useDebounce** — 검색 input 300ms 디바운스"),
    19: ("Next.js",             "Server Actions & API Routes",
         "**① API Route** — /api/todos GET/POST\n**② Server Action** — form 제출로 DB 저장\n**③ 차이 비교** — 언제 뭘 쓸지 정리"),
    20: ("Nuxt 3",              "Nuxt Server Routes & API",
         "**① server/api** — GET/POST 엔드포인트\n**② $fetch** — 클라이언트에서 API 호출\n\n```ts\nexport default defineEventHandler(async (event) => {\n  return [{ id: 1, name: '홍길동' }];\n});\n```"),
    21: ("React + Vitest",      "Vitest로 테스트 작성하기",
         "**① 유틸 함수 테스트** — 1000 → '1,000원' 포맷 함수\n**② 컴포넌트 테스트** — 클릭 시 카운터 증가\n**③ 비동기 테스트** — API 모킹 후 데이터 로딩"),
    22: ("React",               "성능 최적화 — 메모이제이션",
         "**① React.memo** — props 안 바뀌면 리렌더링 방지\n**② useMemo** — 무거운 계산 캐싱\n**③ useCallback** — 함수 메모이제이션\n**④ DevTools Profiler**로 전/후 비교\n\n💬 무조건 메모이제이션이 좋을까요?"),
    23: ("React",               "접근성(A11y) 적용하기",
         "**① 키보드 접근** — Tab/Enter/Escape로 모달 제어\n**② ARIA** — aria-label, aria-expanded, role\n**③ VoiceOver**로 읽히는지 테스트"),
    24: ("React 또는 Next.js",  "포트폴리오 기획 & 설계",
         "나만의 포트폴리오 사이트를 기획해보세요!\n\n**① 사이트 구조** — 페이지/섹션 구성\n**② 기술 스택** — 프레임워크, 라이브러리\n**③ 와이어프레임** — 스케치 or Figma\n**④ 차별점** — 다른 포트폴리오와 다르게 만들 포인트\n\n24주 수고 많으셨어요! 🎉"),
}

FRIDAY_PROBLEMS = {
    1:  ("HTML + CSS",                  "CSS 키프레임으로 카드 UI 만들기",
         "**① 진입 시** fade + slide up 애니메이션\n**② hover 시** 위로 떠오르는 효과\n**③ 버튼 클릭 시** 흔들리는 shake 효과\n\n🎯 `animation`, `transition`, `transform` 세 가지 모두 사용!"),
    2:  ("Vue 3",                       "Vue Transition으로 탭 전환",
         "**① 탭 3개** — 소개, 경력, 연락처\n**② 전환 시** fade + slide 애니메이션\n**③ 방향에 따라** 좌/우 슬라이드"),
    3:  ("React + Framer Motion",       "카드 리스트 stagger 애니메이션",
         "**① stagger** — 카드들이 순차적으로 등장\n**② whileHover** — scale 업\n**③ whileTap** — 눌리는 효과"),
    4:  ("HTML + GSAP",                 "GSAP 타임라인 인트로",
         "**① 제목** — 글자 하나씩 등장\n**② 서브텍스트** — 제목 후 페이드인\n**③ 버튼** — 마지막에 아래서 등장"),
    5:  ("Next.js + Framer Motion",     "페이지 전환 애니메이션",
         "**① 3개 페이지** — /, /about, /work\n**② 전환 시** 현재 페이지 왼쪽, 새 페이지 오른쪽 등장\n**③ AnimatePresence** 적용"),
    6:  ("GSAP + ScrollTrigger",        "스크롤 진입 애니메이션",
         "**① 3개 이상 섹션**\n**② 스크롤 진입 시** 순차 등장\n**③ pin 효과** — 고정 후 내부 요소 애니메이션"),
    7:  ("Vue 3 + TransitionGroup",     "리스트 추가/삭제 애니메이션",
         "**① 추가 시** 위에서 아래로 슬라이드\n**② 삭제 시** 오른쪽으로 밀리며 사라짐\n**③ 이동 시** FLIP 애니메이션"),
    8:  ("React + Framer Motion",       "드래그 앤 드롭",
         "**① 자유 드래그**\n**② dragConstraints** — 영역 제한\n**③ Todo → Done** 카드 이동"),
    9:  ("Vue 3 + GSAP",                "마이크로 인터랙션 버튼",
         "**① 마그네틱 버튼** — 마우스가 끌려오는 효과\n**② Ripple** — 클릭 지점에서 퍼지는 효과\n**③ 텍스트 호버** — 위아래로 교체"),
    10: ("React + Framer Motion",       "모달 & 토스트 애니메이션",
         "**① 모달** — 배경 페이드 + 박스 스프링\n**② 닫기** — 역방향 애니메이션\n**③ 토스트** — 우하단 등장, 3초 후 자동 사라짐"),
    11: ("GSAP + ScrollTrigger",        "스크롤 기반 랜딩 페이지",
         "**① Hero** — 패럴랙스\n**② About** — 텍스트 한 줄씩 등장\n**③ Work** — 가로 스크롤 갤러리\n**④ 스크롤 진행 바**"),
    12: ("React 또는 Vue",              "실전 클론 — 자유 선택",
         "지금까지 배운 것을 모두 활용해 실제 사이트를 클론!\n\n추천: Apple / Linear / Stripe\n\n✅ 진입 애니메이션 ✅ 스크롤 애니메이션 ✅ hover 인터랙션 ✅ 반응형"),
    13: ("Three.js",                    "Three.js 기초 — 3D 오브젝트",
         "**① Scene, Camera, Renderer** 기본 구성\n**② BoxGeometry, SphereGeometry** + Material\n**③ requestAnimationFrame** 회전\n**④ AmbientLight, DirectionalLight** 조명"),
    14: ("HTML + Lottie",               "Lottie 애니메이션 활용",
         "**① lottiefiles.com** 에서 무료 애니메이션 다운\n**② autoplay, loop** 설정\n**③ hover 시 재생, 클릭 시 정지**\n**④ setSpeed()** 속도 조절"),
    15: ("HTML + CSS",                  "CSS 3D 플립 카드",
         "**① 앞면/뒷면** 각각 다른 내용\n**② hover 시** Y축 180도 회전\n**③ backface-visibility** 적용\n**④ 4개 이상 그리드 배치**"),
    16: ("HTML + CSS + GSAP",           "SVG 패스 드로잉 애니메이션",
         "**① stroke-dashoffset** 으로 선 그리기 효과\n**② 로고 패스** 순서대로 그려지기\n**③ 스크롤 연동** — 내릴수록 그려짐"),
    17: ("HTML + GSAP",                 "커스텀 커서 인터랙션",
         "**① 커서** 부드럽게 따라다니기\n**② 링크 hover** 시 커지거나 색 변경\n**③ 클릭** 시 잠깐 작아졌다 돌아옴\n**④ 특정 영역** 커서 안에 텍스트 표시"),
    18: ("Vue 3 + GSAP",                "무한 수평 스크롤 갤러리",
         "**① 무한 루프** — 복사본 이어붙이기\n**② hover 시** 속도 느려짐\n**③ 두 줄이 반대 방향** 으로 흐름"),
    19: ("HTML + Canvas",               "Canvas 파티클 효과",
         "**① 랜덤 파티클** 움직이기\n**② 마우스 근처** 파티클 밀려남\n**③ 가까운 파티클끼리** 선으로 연결"),
    20: ("GSAP",                        "텍스트 & 카운터 애니메이션",
         "**① 글자 단위 순차 등장**\n**② 숫자 카운터** 0 → 목표값\n**③ 타임라인** 으로 두 가지 연결"),
    21: ("React + Recharts",            "인터랙티브 차트",
         "**① 라인 차트** — 월별 방문자 수\n**② 바 차트** — 카테고리별 매출\n**③ 커스텀 툴팁**\n**④ 반응형** 대응"),
    22: ("React + Framer Motion",       "3D 카드 틸트 + 글로우",
         "**① 마우스 위치** 따라 X/Y 기울기\n**② 반사광** 그라디언트 효과\n**③ 스프링 물리** — 원위치 복귀"),
    23: ("GSAP + ScrollTrigger",        "풀페이지 스크롤",
         "**① 섹션 스냅** 이동\n**② 진행 인디케이터** (우측 점)\n**③ 섹션별 진입 애니메이션**\n**④ 방향키** 지원"),
    24: ("React 또는 Vue",              "포트폴리오 랜딩 페이지 완성",
         "✅ Hero (진입 애니메이션)\n✅ About (스크롤 애니메이션)\n✅ Works (hover 인터랙션)\n✅ Contact\n✅ 반응형 + 다크모드\n⭐ 커스텀 커서\n⭐ 페이지 전환\n⭐ 스크롤 진행 바\n\n24주 수고 많으셨어요! 🎉🎊"),
}


def get_week(start_date):
    now = datetime.now(KST)
    diff = (now - start_date).days
    if diff < 0:
        return None
    week = diff // 7 + 1
    return week if 1 <= week <= 24 else None


intents = discord.Intents.default()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler(timezone=KST)


async def send_tuesday():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("채널을 찾을 수 없어요.")
        return
    week = get_week(START_TUESDAY)
    if not week:
        print(f"커리큘럼 범위 밖")
        return
    tool, topic, content = TUESDAY_PROBLEMS[week]
    deadline = (datetime.now(KST) + timedelta(days=3)).strftime("%Y년 %-m월 %-d일")
    embed = discord.Embed(
        title=f"📌 {week}주차 화요일 문제 — 개념편",
        color=0x58A6FF
    )
    embed.add_field(name="🛠 사용 도구", value=f"**{tool}**", inline=False)
    embed.add_field(name=f"문제: {topic}", value=content, inline=False)
    embed.add_field(name="⏰ 기한", value=f"**{deadline}** 자정까지\nStackBlitz 링크를 이 채널에 공유해주세요!", inline=False)
    embed.set_footer(text=f"{week}주차 / 화요일 / {tool} | 모르면 언제든 질문하세요 💪")
    await channel.send(embed=embed)
    print(f"{week}주차 화요일 문제 전송 완료")


async def send_friday():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("채널을 찾을 수 없어요.")
        return
    week = get_week(START_FRIDAY)
    if not week:
        print(f"커리큘럼 범위 밖")
        return
    tool, topic, content = FRIDAY_PROBLEMS[week]
    deadline = (datetime.now(KST) + timedelta(days=3)).strftime("%Y년 %-m월 %-d일")
    embed = discord.Embed(
        title=f"🎨 {week}주차 금요일 문제 — UI + 모션편",
        color=0xF1C40F
    )
    embed.add_field(name="🛠 사용 도구", value=f"**{tool}**", inline=False)
    embed.add_field(name=f"문제: {topic}", value=content, inline=False)
    embed.add_field(name="⏰ 기한", value=f"**{deadline}** 자정까지\nStackBlitz 또는 CodePen 링크를 이 채널에 공유해주세요!", inline=False)
    embed.set_footer(text=f"{week}주차 / 금요일 / {tool} | 퍼블리싱 실력 발휘할 차례예요 🎨")
    await channel.send(embed=embed)
    print(f"{week}주차 금요일 문제 전송 완료")


@client.event
async def on_ready():
    print(f"봇 로그인: {client.user}")
    scheduler.add_job(send_tuesday, "cron", day_of_week="tue", hour=8, minute=0)
    scheduler.add_job(send_friday,  "cron", day_of_week="fri", hour=8, minute=0)
    scheduler.start()
    print("스케줄러 시작 — 화요일/금요일 오전 8시 KST")


client.run(TOKEN)
