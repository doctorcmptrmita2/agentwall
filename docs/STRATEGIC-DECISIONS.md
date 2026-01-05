# AgentGuard & Monitor - Strategic Decisions & Architecture

**Date:** 5 Ocak 2026  
**Decision Maker:** CTO & Lead Architect  
**Status:** APPROVED - Ready for Implementation

---

## 🎯 EXECUTIVE SUMMARY

Bu belge, AgentGuard & Monitor projesinin kritik stratejik kararlarını içerir. Web araştırması ve pazar analizi sonuçlarına dayanarak, **"Agent Firewall"** konumlandırması ile ilerleme kararı alınmıştır.

**Core Decision:** Standalone "Agent Firewall" olarak başla, traction sonrası plugin/vertical SaaS pivot seçeneği aç.

---

## 🔍 KARAR 1: Farklılaşma Stratejisi

### Problem
Rakipler (LiteLLM, Portkey, Helicone) "LLM Gateway" olarak konumlanmış. Biz neden farklıyız?

### Araştırma Bulguları

**Loop Detection Teknikleri (Kaynak: Maxim AI, Invariant Labs):**
- Multi-turn pattern detection (aynı prompt/output döngüsü)
- Step counting (maksimum adım limiti)
- Cosine similarity (tekrar eden içerik tespiti)
- Tool call frequency analysis (aynı tool'u 10+ kez çağırma)

**Rakip Analizi:**
- **LiteLLM:** Cost tracking var, ama run-level budget YOK
- **Portkey:** Guardrails var, ama tool governance YOK
- **Helicone:** Observability güçlü, ama loop detection YOK
- **Kong:** Enterprise-grade, ama AI-specific özellikler zayıf

### ✅ KARAR: "Agent Firewall" Konumlandırması

**Farklılaşma Pillars:**

1. **Run-Level Intelligence** (Rakiplerde YOK)
   - Tek request değil, tüm agent görevi izleme
   - Run budget: "$0.50 geçerse durdur"
   - Step limit: "30 LLM çağrısı maksimum"
   - Wall-clock timeout: "2 dakika maksimum"

2. **Loop Detection Engine** (Rakiplerde YOK)
   - Cosine similarity (prompt/output tekrarı)
   - Tool call frequency (aynı tool 5+ kez)
   - State repetition (aynı durum 3+ kez)
   - Auto-kill switch (anomali tespit edilince)

3. **Tool Governance** (Rakiplerde YOK)
   - Policy-as-Code: "Bu agent şu tool'u çağırabilir"
   - Allowlist/denylist: Domain, IP, endpoint sınırları
   - Approval gates: Kritik aksiyonlar insan onayı ister
   - Sandbox mode: Test ortamında güvenli çalıştırma

4. **Incident Replay** (Rakiplerde YOK)
   - Trace ID ile tüm run'ı kaydet
   - Dashboard'da "Replay" butonu
   - "Bu adımda leak oldu" → one-click policy
   - Rollback: "Kuralı devreye al, yeniden başlat"

### ADR-001: Neden "Agent Firewall" değil "LLM Gateway"?

**Context:** LLM Gateway pazarı kalabalık (5+ güçlü rakip).

**Decision:** "Agent Firewall" olarak konumlan.

**Rationale:**
- Agent'lar 2026'da patlama yapıyor (Gartner: %40 enterprise adoption)
- Sonsuz döngü = #1 korku (maliyet patlaması)
- Rakipler "tek request" odaklı, biz "run" odaklıyız
- Moat: Agent-run semantiği anlamak teknik bariyer

**Consequences:**
- ✅ Daha dar, derin odak
- ✅ Daha yüksek fiyatlandırma ($199/ay vs $49/ay)
- ✅ Daha güçlü moat (kopyalanması zor)
- ⚠️ Daha küçük initial market (agent kullananlar)

---

## 🎯 KARAR 2: Go-to-Market Stratejisi

### Problem
Hangi segment önce? SaaS, ajans, finans, sağlık?

### Araştırma Bulguları

**B2B SaaS GTM Best Practices:**
- İlk müşteri: "En acı çeken" segment
- Uzun satış döngüsü: 3-6 ay (enterprise)
- Kısa satış döngüsü: 1-2 hafta (SMB)
- Product-led growth: Free trial → paid conversion

**AI Agent Market 2026:**
- %68.9 content production agents (en yaygın)
- %40 enterprise adoption (Gartner)
- $103.6B market (2032'ye kadar)
- En hızlı büyüyen: Customer support, sales, dev tools

### ✅ KARAR: 3-Tier GTM Strategy

#### Tier 1: AI-Powered SaaS Companies (İlk 3 Ay)

**Neden önce?**
- En acı çeken segment (maliyet patlaması yaşıyorlar)
- Kısa satış döngüsü (1-2 hafta)
- Teknik ekip var (entegrasyon kolay)
- Recurring revenue (MRR predictable)

**Hedef Profil:**
- Customer support agents (Intercom, Zendesk benzeri)
- Content generation agents (Jasper, Copy.ai benzeri)
- Dev tools agents (GitHub Copilot benzeri)
- 10-50 kişi, $1M-$10M ARR

**GTM Tactics:**
- Product Hunt launch (Top 5 hedef)
- AI communities (Reddit r/LangChain, Discord)
- Content marketing (loop detection case studies)
- Free tier (1K requests/ay)

#### Tier 2: Agencies & Automation Teams (3-6 Ay)

**Neden ikinci?**
- Müşteri datası hassas (DLP değerli)
- Maliyet hassas (budget tracking değerli)
- Çok agent kullanıyorlar (volume yüksek)

**Hedef Profil:**
- Marketing agencies (AI content üretimi)
- RPA/automation consultants
- AI implementation partners
- 5-20 kişi, $500K-$5M revenue

**GTM Tactics:**
- Partner program (20% commission)
- White-label option (agency branding)
- Case studies (maliyet tasarrufu)

#### Tier 3: Regulated Industries (6-12 Ay)

**Neden son?**
- Uzun satış döngüsü (6-12 ay)
- Compliance requirements (HIPAA, SOC2)
- Yüksek fiyatlandırma ($2K-$10K/ay)
- Daha fazla domain expertise gerekir

**Hedef Profil:**
- Fintech (PCI-DSS)
- Healthcare (HIPAA)
- Legal (attorney-client privilege)

**GTM Tactics:**
- Compliance certifications (SOC2, ISO 27001)
- Enterprise sales team
- Custom contracts (BAA, DPA)

### ADR-002: Neden SaaS önce, finans/sağlık son?

**Context:** Sermaye sınırlı ($50K), hızlı traction gerekli.

**Decision:** SaaS → Agencies → Regulated Industries

**Rationale:**
- SaaS: Kısa satış döngüsü (1-2 hafta), teknik ekip var
- Agencies: Orta satış döngüsü (1 ay), volume yüksek
- Regulated: Uzun satış döngüsü (6-12 ay), compliance gerekir

**Consequences:**
- ✅ Hızlı ilk müşteri (3 ay içinde 10 paying)
- ✅ Hızlı feedback loop (product iteration)
- ⚠️ Daha düşük initial ARPU ($49-$199 vs $2K+)

---

## 🏗️ KARAR 3: Positioning Strategy

### Problem
Standalone mı, plugin mi, vertical SaaS mi?

### Araştırma Bulguları

**Standalone Gateway:**
- ✅ Tam kontrol (product roadmap)
- ✅ Daha yüksek valuation (exit)
- ⚠️ Daha yavaş adoption (switching cost)
- ⚠️ Daha fazla competition

**Plugin/Add-on:**
- ✅ Hızlı adoption (mevcut kullanıcı tabanı)
- ✅ Daha az competition (tamamlayıcı)
- ⚠️ Bağımlılık (LiteLLM değişirse etkileniriz)
- ⚠️ Daha düşük valuation

**Vertical SaaS:**
- ✅ Daha yüksek fiyatlandırma ($500-$2K/ay)
- ✅ Daha derin moat (compliance expertise)
- ⚠️ Daha uzun satış döngüsü
- ⚠️ Daha fazla domain bilgisi

### ✅ KARAR: Hybrid Strategy (Standalone → Plugin Pivot Option)

**Phase 1 (0-6 Ay): Standalone "Agent Firewall"**

**Neden?**
- Tam kontrol (product vision)
- Farklılaşma net (agent-run semantiği)
- Exit potansiyeli yüksek (Kong, Cloudflare satın alabilir)

**MVP Features:**
- OpenAI-compatible endpoint
- Run-level budget + loop breaker
- Basic DLP (regex/pattern)
- Simple dashboard

**Phase 2 (6-12 Ay): Plugin Option (Traction'a Göre)**

**Pivot Trigger:**
- Eğer adoption yavaşsa (<50 paying customers)
- Eğer LiteLLM/Portkey dominant olursa
- Eğer switching cost çok yüksekse

**Plugin Strategy:**
- "LiteLLM Agent Firewall Plugin"
- "Portkey Loop Detection Add-on"
- "Helicone Tool Governance Extension"

**Phase 3 (12+ Ay): Vertical SaaS Option**

**Pivot Trigger:**
- Eğer regulated industry traction güçlüyse
- Eğer compliance expertise kazanırsak
- Eğer ARPU $500+ olursa

**Vertical Options:**
- "Healthcare AI Agent Compliance Platform"
- "Financial Services AI Firewall"

### ADR-003: Neden Standalone başla, pivot option aç?

**Context:** Pazar belirsiz, rekabet yoğun.

**Decision:** Standalone başla, 6 ayda pivot değerlendir.

**Rationale:**
- Standalone: Maksimum kontrol + exit potansiyeli
- Pivot option: Risk azaltma (adoption yavaşsa)
- 6 ay: Yeterli data (traction ölçümü için)

**Consequences:**
- ✅ Maksimum upside (standalone başarılıysa)
- ✅ Downside protection (pivot option varsa)
- ⚠️ Daha fazla initial effort (standalone kurmak)

---

## 🛠️ KARAR 4: Technical Architecture

### Core Stack Decision

**FastAPI (Proxy Engine):**
- ✅ Async/await (high throughput)
- ✅ Pydantic V2 (validation)
- ✅ Python ecosystem (LangChain, tiktoken)
- Target: <10ms overhead

**Laravel (Dashboard):**
- ✅ Filament (admin panel)
- ✅ Livewire (real-time UI)
- ✅ Multi-tenancy (team isolation)
- Target: <100ms response time

**Database:**
- PostgreSQL (relational: users, policies)
- ClickHouse (time-series: logs, analytics)
- Redis (rate limiting, caching)

### ADR-004: Neden ClickHouse logs için?

**Context:** Milyonlarca log, veritabanı şişmesi riski.

**Decision:** ClickHouse (columnar database) kullan.

**Rationale:**
- 100x daha hızlı (time-series queries)
- Otomatik partitioning (eski loglar archive)
- Compression (10x daha az disk)
- Laravel'den query kolay (HTTP API)

**Consequences:**
- ✅ Ölçeklenebilir (milyonlarca log)
- ✅ Hızlı analytics (dashboard <100ms)
- ⚠️ Ekstra infra (ClickHouse cluster)

---

## 🚀 IMPLEMENTATION ROADMAP

### Week 1: FastAPI Proxy Core

**Goal:** OpenAI-compatible endpoint + basic logging

**Tasks:**
1. FastAPI project setup
2. OpenAI proxy endpoint (`/v1/chat/completions`)
3. API key authentication (Redis)
4. Request/response logging (ClickHouse)
5. Streaming support (SSE)

**Success Criteria:**
- ✅ Drop-in replacement (base_url değiştir, çalış)
- ✅ <10ms overhead
- ✅ Streaming bozulmasın

### Week 2: Agent Firewall Features

**Goal:** Run-level budget + loop detection

**Tasks:**
1. Run tracking (trace ID, step counter)
2. Budget calculator (tiktoken + pricing)
3. Loop detector (cosine similarity)
4. Auto-kill switch (budget/step limit aşımı)
5. DLP engine (regex: API keys, credit cards)

**Success Criteria:**
- ✅ Sonsuz döngü 30 step'te dursun
- ✅ Budget $0.50 aşınca dursun
- ✅ API key sızıntısı engellensin

### Week 3: Laravel Dashboard

**Goal:** User management + analytics

**Tasks:**
1. Laravel + Filament setup
2. User/team management
3. API key generation
4. Dashboard: Spend, blocked requests, top agents
5. Alerts (webhook/Slack)

**Success Criteria:**
- ✅ Kullanıcı 2 dakikada kayıt olup API key alsın
- ✅ Dashboard <100ms response time
- ✅ Real-time alerts (budget aşımı)

---

## 📊 SUCCESS METRICS

### MVP Validation (3 Ay)

- ✅ 50 aktif kullanıcı (free + paid)
- ✅ 10 ödeme yapan müşteri ($500 MRR)
- ✅ %20 free-to-paid conversion
- ✅ 1 "prevented cost blowup" success story
- ✅ Product Hunt: Top 5

### Product-Market Fit (6 Ay)

- ✅ 500 aktif kullanıcı
- ✅ 50 ödeme yapan müşteri ($10K MRR)
- ✅ %10 churn (aylık)
- ✅ NPS > 40
- ✅ 2-3 case study

### Pivot Decision Point (6 Ay)

**IF traction güçlü:**
- Continue standalone
- Scale to Tier 2 (agencies)
- Hire sales team

**IF traction zayıf:**
- Pivot to plugin strategy
- Partner with LiteLLM/Portkey
- Focus on tool governance niche

---

## 🎬 NEXT ACTIONS

### Immediate (Bu Hafta)

1. ✅ Strategic decisions document (BU BELGE)
2. ⏳ FastAPI project skeleton
3. ⏳ OpenAI proxy middleware design
4. ⏳ ClickHouse schema design
5. ⏳ Laravel project setup

### Short-term (2-3 Hafta)

1. MVP development (Week 1-3 roadmap)
2. Beta testing (10 early adopters)
3. Product Hunt launch prep
4. Pricing page + landing page

### Medium-term (3-6 Ay)

1. First 10 paying customers
2. Case studies (loop detection saves)
3. Tier 2 GTM (agencies)
4. Fundraising prep (seed deck)

---

**Approved by:** CTO & Lead Architect  
**Date:** 5 Ocak 2026  
**Status:** READY FOR IMPLEMENTATION

**Motto:** "Guard the Agent, Save the Budget"
