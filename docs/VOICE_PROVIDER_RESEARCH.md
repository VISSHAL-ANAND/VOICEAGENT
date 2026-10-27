# Voice and Telephony Provider Research

**Research date:** 2026-10-28  
**Status:** Preliminary desk research only — no provider selected, account created, API key issued, phone number purchased, or paid service activated.

## Requirements to evaluate

The production solution needs an Indian inbound phone number, real-time call audio streaming, call lifecycle controls and manager transfer, plus voice processing for Tamil, Hindi, English, Kannada, and Telugu. It must connect to VoiceAgent's own backend so property data and booking rules remain authoritative. Local/mock development remains ₹0.

## Findings from official provider information

### Exotel AgentStream — candidate for Indian telephony/audio transport

Official pages:
- AgentStream: https://www.exotel.com/products/agentstream-voice-streaming/
- Developer docs: https://developer.exotel.com/
- ExoPhone setup and billing: https://developer.exotel.com/docs/getting-started/exophone-setup
- SIP trunking / voice AI guide: https://docs.exotel.com/dynamic-sip-trunking/flow-and-api-configuration-guide-for-voice-ai-and-contact-centre-platforms

What the published material supports:
- Exotel describes ExoPhones as virtual numbers that receive inbound calls.
- AgentStream advertises real-time audio streaming and live call control for voice agents; the published product page describes PCM 16-bit audio at 16 kHz by default and 24 kHz availability.
- The developer documentation demonstrates a call connection API using a WebSocket stream URL.
- Exotel's published setup guide describes recurring number rental and inbound-call charges.

Not yet verified:
- Exact account eligibility, sandbox restrictions, number availability for this use case/city, actual price quote, manager transfer behavior for the intended call flow, and the exact integration contract we would use.
- Product marketing claims are not a substitute for a successful test call or contractual service-level agreement.

### Nia Voice — candidate for realtime multilingual speech/voice processing

Official pages:
- Product: https://niavoices.com/
- API docs: https://niavoices.com/docs
- Pricing: https://niavoices.com/pricing
- Terms: https://niavoices.com/terms

What the published material supports:
- Nia documents a real-time two-way voice API and a mode intended to use an external/custom LLM, which could allow VoiceAgent's backend to retain control over property lookup and booking logic.
- The product page lists Tamil, Hindi, English, Kannada, and Telugu among its supported speech languages.
- Its documentation says access is invite-only while the service scales.
- The terms describe usage-based billing/credits and state that beta endpoints may change.

Not yet verified:
- Current exact free allotment and paid per-minute cost, invite availability, production limits, latency/accuracy in all five required languages, and how the provider's WebRTC real-time session would be bridged to a PSTN phone call through a telephony provider.
- Claims about audio storage and language quality need to be checked against the current terms, configuration, and a measured test; they are not yet accepted as our privacy or quality policy.

### Vakyam AI — candidate for streaming text-to-speech, not a complete voice agent

Official pages:
- Docs: https://docs.vakyam.ai/
- Pricing: https://docs.vakyam.ai/pricing
- Realtime WebSocket: https://docs.vakyam.ai/guides/realtime-websocket

What the published material supports:
- Its Raaga TTS documents English, Hindi, Tamil, Telugu, and Kannada.
- A Free plan is listed at ₹0/month with 10,000 characters/month (approximately 13 minutes of generated audio), one concurrent request, and 15 requests/minute.
- The WebSocket API streams generated audio sentence-by-sentence.

Important limitation:
- This is TTS, not by itself the complete speech-recognition + conversation + telephony system. We would still need a speech-to-text/realtime conversation component and telephony transport. A free quota is subject to provider terms and limits and does not make the entire phone agent free.

### Twilio — comparison reference, not currently a preferred India-number option

Official page: https://www.twilio.com/en-us/voice/pricing/in

The official India pricing page publishes per-minute prices for several voice features, including media streams, and lists international number pricing starting at US$1.15/month. That page alone does **not** prove that the specific Indian inbound number, AI media-streaming route, or active-call transfer required by this project is available to this account. Those capabilities and any India-specific restrictions must be verified before considering Twilio.

## Preliminary comparison

| Candidate | Potential role | Five target languages | Free development path | Main open question |
|---|---|---|---|---|
| Exotel AgentStream | Indian number, call transport, live audio/call control | Telephony is language-neutral; the speech engine must be evaluated separately | Sandbox is advertised; actual limits/eligibility need confirmation | Exact account/number eligibility, price, and transfer behavior |
| Nia Voice | Realtime speech/voice with custom backend option | Listed on product materials; quality must be measured | Access is invite-only; current free allowance needs confirmation | Access, cost, PSTN bridge, measured quality |
| Vakyam AI | Streaming TTS output | All five are listed for TTS | Free plan: 10k characters/month, one concurrent request | Need separate speech recognition/conversation and telephony |
| Twilio | Telephony/media-streaming comparison | Speech engine separate | Pricing is usage-based; not a zero-cost production path by default | India inbound number and exact required call-control eligibility |

## Recommended next evaluation — not a vendor decision

1. Ask Exotel for confirmation of sandbox access, Indian inbound-number eligibility, AgentStream/WebSocket access, live transfer API support, and a written cost estimate for a small pilot.
2. If access is available, evaluate the speech layer independently using synthetic prompts and a fixed test set for Tamil, Hindi, English, Kannada, and Telugu.
3. Keep property lookup and reservation actions behind VoiceAgent's backend. Never let a voice provider's default brain invent availability or confirm a booking.
4. Before any account setup requiring payment, number rental, top-up, or binding commitment, obtain explicit user approval.
5. Do not send real guest audio or personal data to a provider before the client approves the data flow and recording/retention policy.

## Decision status

No provider choice is made by this research. This is a documented shortlist from public official information, not proof of integration, compliance, price, or production readiness.
