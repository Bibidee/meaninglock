# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""MeaningLock — standalone semantic-covenant escrow for GenLayer.

Only this file is deployable. Tests are deliberately not contract neighbours.
"""
from genlayer import *
from datetime import datetime, timezone

MAX_LABEL_CHARS=128
MAX_STATEMENT_CHARS=4000
MAX_TOPICS_CHARS=1000
MAX_REASON_CHARS=2000
MAX_DESCRIPTION_CHARS=4000
MAX_URL_CHARS=2048
MAX_EVIDENCE_REFERENCES=64
MAX_AUDIT_RECORDS=256
MAX_APPEALS=2
TOPIC_MASK_MAX=u256(255)

NONE=u256(0)
PRESERVED=u256(1)
CHANGED=u256(2)
REMOVED=u256(3)
UNVERIFIABLE=u256(4)
CANCELLED=u256(5)
EXPIRED=u256(6)
ACTIVE=u256(1)
PENDING=u256(2)
RESOLVED=u256(3)
CLOSED=u256(4)
LOW=u256(0)
MEDIUM=u256(1)
HIGH=u256(2)
NO_IMPACT=u256(0)
MINOR=u256(1)
MATERIAL=u256(2)
CRITICAL=u256(3)

@gl.evm.contract_interface
class _Recipient:
    class View: pass
    class Write: pass

class MeaningLock(gl.Contract):
    """Escrowed promise whose current public meaning is independently assessed.

    The contract stores only metadata and a categorical consensus result. Raw
    content is fetched on demand by every validator, avoiding stale data and
    avoiding large/unstable state. Any `UNVERIFIABLE` result has a timeout
    recovery path
    it can never by itself select an adverse payout.
    """
    owner: Address
    paused: bool
    minimum_bond: u256
    challenge_window: u256
    recovery_window: u256
    count: u256
    publisher: TreeMap[u256, Address]
    beneficiary: TreeMap[u256, Address]
    live_url: TreeMap[u256, str]
    baseline_url: TreeMap[u256, str]
    baseline_image_url: TreeMap[u256, str]
    statement: TreeMap[u256, str]
    topics: TreeMap[u256, str]
    label: TreeMap[u256, str]
    state: TreeMap[u256, u256]
    verdict: TreeMap[u256, u256]
    impact: TreeMap[u256, u256]
    confidence: TreeMap[u256, u256]
    topic_mask: TreeMap[u256, u256]
    expires_at: TreeMap[u256, u256]
    challenged_at: TreeMap[u256, u256]
    challenge_deadline: TreeMap[u256, u256]
    recovery_deadline: TreeMap[u256, u256]
    checked_at: TreeMap[u256, u256]
    round: TreeMap[u256, u256]
    challenger: TreeMap[u256, Address]
    reason: TreeMap[u256, str]
    challenge_url: TreeMap[u256, str]
    challenge_image_url: TreeMap[u256, str]
    publisher_bond: TreeMap[u256, u256]
    beneficiary_bond: TreeMap[u256, u256]
    challenger_bond: TreeMap[u256, u256]
    escrow: TreeMap[u256, u256]
    paid: TreeMap[u256, bool]
    paid_to: TreeMap[u256, Address]
    paid_amount: TreeMap[u256, u256]
    note: TreeMap[u256, str]
    description: TreeMap[u256, str]
    source_version: TreeMap[u256, u256]
    minimum_confidence: TreeMap[u256, u256]
    permitted_impact: TreeMap[u256, u256]
    visual_required: TreeMap[u256, bool]
    fallback_allowed: TreeMap[u256, bool]
    settlement_publisher_bps: TreeMap[u256, u256]
    settlement_beneficiary_bps: TreeMap[u256, u256]
    settlement_challenger_bps: TreeMap[u256, u256]
    evidence_count: TreeMap[u256, u256]
    evidence_kind: TreeMap[u256, str]
    evidence_url: TreeMap[u256, str]
    evidence_digest: TreeMap[u256, str]
    evidence_submitted_at: TreeMap[u256, u256]
    appeal_count: TreeMap[u256, u256]
    appeal_deadline: TreeMap[u256, u256]
    appeal_reason: TreeMap[u256, str]
    appeal_url: TreeMap[u256, str]
    appeal_image_url: TreeMap[u256, str]
    appeal_bond: TreeMap[u256, u256]
    audit_count: TreeMap[u256, u256]
    audit_action: TreeMap[u256, str]
    audit_actor: TreeMap[u256, Address]
    audit_time: TreeMap[u256, u256]
    audit_note: TreeMap[u256, str]

    def __init__(self, minimum_bond: u256, challenge_window: u256, recovery_window: u256):
        self.owner=gl.message.sender_address
        self.paused=False
        self.minimum_bond=minimum_bond
        self.challenge_window=challenge_window
        self.recovery_window=recovery_window
        self.count=u256(0)
        self.publisher=gl.storage.inmem_allocate(TreeMap[u256, Address])
        self.beneficiary=gl.storage.inmem_allocate(TreeMap[u256, Address])
        self.live_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.baseline_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.baseline_image_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.statement=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.topics=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.label=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.state=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.verdict=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.impact=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.confidence=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.topic_mask=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.expires_at=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.challenged_at=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.challenge_deadline=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.recovery_deadline=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.checked_at=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.round=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.challenger=gl.storage.inmem_allocate(TreeMap[u256, Address])
        self.reason=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.challenge_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.challenge_image_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.publisher_bond=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.beneficiary_bond=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.challenger_bond=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.escrow=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.paid=gl.storage.inmem_allocate(TreeMap[u256, bool])
        self.paid_to=gl.storage.inmem_allocate(TreeMap[u256, Address])
        self.paid_amount=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.note=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.description=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.source_version=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.minimum_confidence=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.permitted_impact=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.visual_required=gl.storage.inmem_allocate(TreeMap[u256, bool])
        self.fallback_allowed=gl.storage.inmem_allocate(TreeMap[u256, bool])
        self.settlement_publisher_bps=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.settlement_beneficiary_bps=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.settlement_challenger_bps=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.evidence_count=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.evidence_kind=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.evidence_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.evidence_digest=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.evidence_submitted_at=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.appeal_count=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.appeal_deadline=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.appeal_reason=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.appeal_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.appeal_image_url=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.appeal_bond=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.audit_count=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.audit_action=gl.storage.inmem_allocate(TreeMap[u256, str])
        self.audit_actor=gl.storage.inmem_allocate(TreeMap[u256, Address])
        self.audit_time=gl.storage.inmem_allocate(TreeMap[u256, u256])
        self.audit_note=gl.storage.inmem_allocate(TreeMap[u256, str])

    @gl.public.write
    def set_paused(self, paused: bool) -> None:
        self._owner()
        self.paused=paused

    @gl.public.write
    def set_windows(self, challenge_window: u256, recovery_window: u256) -> None:
        self._owner()
        if challenge_window==u256(0) or recovery_window==u256(0): raise gl.vm.UserError("window must be positive")
        self.challenge_window=challenge_window
        self.recovery_window=recovery_window

    @gl.public.write.payable
    def register_covenant(self, label: str, live_url: str, baseline_url: str, baseline_image_url: str, statement: str, topics: str, beneficiary: Address, expires_at: u256) -> u256:
        beneficiary = Address(beneficiary)
        if self.paused: raise gl.vm.UserError("paused")
        self._text(label,"label")
        self._text(live_url,"live url")
        self._text(baseline_url,"baseline url")
        self._assert_live_url(live_url)
        self._assert_baseline_url(baseline_url)
        self._assert_image_optional(baseline_image_url)
        self._text(statement,"statement")
        self._text(topics,"topics")
        if expires_at<=self._now(): raise gl.vm.UserError("expiry must be future")
        if gl.message.value<self.minimum_bond: raise gl.vm.UserError("insufficient publisher bond")
        i=self.count+u256(1)
        self.count=i
        self.publisher[i]=gl.message.sender_address
        self.beneficiary[i]=beneficiary
        self.live_url[i]=live_url
        self.baseline_url[i]=baseline_url
        self.baseline_image_url[i]=baseline_image_url
        self.statement[i]=statement
        self.topics[i]=topics
        self.label[i]=label
        self.state[i]=ACTIVE
        self.verdict[i]=NONE
        self.impact[i]=NO_IMPACT
        self.confidence[i]=LOW
        self.topic_mask[i]=u256(0)
        self.expires_at[i]=expires_at
        self.challenged_at[i]=u256(0)
        self.challenge_deadline[i]=u256(0)
        self.recovery_deadline[i]=u256(0)
        self.checked_at[i]=u256(0)
        self.round[i]=u256(0)
        self.challenger[i]=Address("0x0000000000000000000000000000000000000000")
        self.reason[i]=""
        self.challenge_url[i]=""
        self.challenge_image_url[i]=""
        self.publisher_bond[i]=gl.message.value
        self.beneficiary_bond[i]=u256(0)
        self.challenger_bond[i]=u256(0)
        self.escrow[i]=gl.message.value
        self.paid[i]=False
        self.paid_amount[i]=u256(0)
        self.note[i]="active"
        self.description[i]=""
        self.source_version[i]=u256(1)
        self.minimum_confidence[i]=MEDIUM
        self.permitted_impact[i]=MATERIAL
        self.visual_required[i]=baseline_image_url!=""
        self.fallback_allowed[i]=True
        self.settlement_publisher_bps[i]=u256(10000)
        self.settlement_beneficiary_bps[i]=u256(0)
        self.settlement_challenger_bps[i]=u256(0)
        self.evidence_count[i]=u256(0)
        self.appeal_count[i]=u256(0)
        self.appeal_deadline[i]=u256(0)
        self.appeal_bond[i]=u256(0)
        self.audit_count[i]=u256(0)
        self._audit(i,"REGISTER",gl.message.sender_address,"covenant created")
        return i

    @gl.public.write.payable
    def add_bond(self, covenant_id: u256, role: u256) -> None:
        self._active(covenant_id)
        if gl.message.value==u256(0): raise gl.vm.UserError("positive value required")
        if role==u256(1):
            self._publisher(covenant_id)
            self.publisher_bond[covenant_id]=self.publisher_bond[covenant_id]+gl.message.value
        else: raise gl.vm.UserError("only publisher may add security collateral")
        self.escrow[covenant_id]=self.escrow[covenant_id]+gl.message.value
        self._audit(covenant_id,"BOND_ADDED",gl.message.sender_address,"additional escrow received")

    @gl.public.write
    def set_covenant_description(self, covenant_id: u256, description: str) -> None:
        """Attach human-readable implementation notes without changing the promise."""
        self._active(covenant_id)
        self._publisher(covenant_id)
        self._text(description, "description")
        self.description[covenant_id] = description
        self.source_version[covenant_id] = self.source_version[covenant_id] + u256(1)
        self._audit(covenant_id, "DESCRIPTION_UPDATED", gl.message.sender_address, "metadata only")

    @gl.public.write
    def configure_evidence_policy(
        self,
        covenant_id: u256,
        minimum_confidence: u256,
        permitted_impact: u256,
        visual_required: bool,
        fallback_allowed: bool,
    ) -> None:
        """Set conservative classification thresholds before a challenge exists."""
        self._active(covenant_id)
        self._publisher(covenant_id)
        if minimum_confidence > HIGH:
            raise gl.vm.UserError("invalid confidence threshold")
        if permitted_impact > CRITICAL:
            raise gl.vm.UserError("invalid impact threshold")
        self.minimum_confidence[covenant_id] = minimum_confidence
        self.permitted_impact[covenant_id] = permitted_impact
        self.visual_required[covenant_id] = visual_required
        self.fallback_allowed[covenant_id] = fallback_allowed
        self._audit(covenant_id, "POLICY_UPDATED", gl.message.sender_address, "evidence policy changed")

    @gl.public.write
    def configure_settlement_split(
        self,
        covenant_id: u256,
        publisher_bps: u256,
        beneficiary_bps: u256,
        challenger_bps: u256,
    ) -> None:
        """Configure deterministic basis-point allocation for adverse settlement."""
        self._active(covenant_id)
        self._publisher(covenant_id)
        if publisher_bps + beneficiary_bps + challenger_bps != u256(10000):
            raise gl.vm.UserError("settlement split must equal 10000 bps")
        self.settlement_publisher_bps[covenant_id] = publisher_bps
        self.settlement_beneficiary_bps[covenant_id] = beneficiary_bps
        self.settlement_challenger_bps[covenant_id] = challenger_bps
        self._audit(covenant_id, "SETTLEMENT_POLICY_UPDATED", gl.message.sender_address, "basis points changed")

    @gl.public.write
    def submit_evidence_reference(
        self,
        covenant_id: u256,
        kind: str,
        url: str,
        digest: str,
    ) -> u256:
        """Record a public evidence pointer
        bytes remain outside contract storage."""
        self._known(covenant_id)
        self._text(kind, "evidence kind")
        self._text(url, "evidence url")
        self._text(digest, "evidence digest")
        if gl.message.sender_address != self.publisher[covenant_id] and gl.message.sender_address != self.beneficiary[covenant_id] and gl.message.sender_address != self.challenger[covenant_id]:
            raise gl.vm.UserError("covenant party only")
        n = self.evidence_count[covenant_id] + u256(1)
        self.evidence_count[covenant_id] = n
        if n > MAX_EVIDENCE_REFERENCES: raise gl.vm.UserError("evidence limit reached")
        key = self._evidence_key_for(n, covenant_id)
        self.evidence_kind[key] = kind
        self.evidence_url[key] = url
        self.evidence_digest[key] = digest
        self.evidence_submitted_at[key] = self._now()
        self._audit(covenant_id, "EVIDENCE_REFERENCED", gl.message.sender_address, kind)
        return n

    @gl.public.write
    def appeal_verdict(
        self,
        covenant_id: u256,
        reason: str,
        evidence_url: str,
        image_url: str,
    ) -> None:
        """Open one bounded appeal
        appeals never transfer funds automatically."""
        self._known(covenant_id)
        self._text(reason, "appeal reason")
        if self.state[covenant_id] != RESOLVED or not self._outcome_is_adverse(self.verdict[covenant_id]):
            raise gl.vm.UserError("adverse resolved covenant required")
        if self.appeal_deadline[covenant_id] != u256(0) and self._deadline_is_open(self.appeal_deadline[covenant_id]):
            raise gl.vm.UserError("appeal window still open")
        if self.paid[covenant_id]:
            raise gl.vm.UserError("settlement already paid")
        if self.appeal_count[covenant_id] >= u256(2):
            raise gl.vm.UserError("appeal limit reached")
        if gl.message.sender_address != self.publisher[covenant_id] and gl.message.sender_address != self.beneficiary[covenant_id] and gl.message.sender_address != self.challenger[covenant_id]:
            raise gl.vm.UserError("covenant party only")
        self.appeal_count[covenant_id] = self.appeal_count[covenant_id] + u256(1)
        self.appeal_reason[covenant_id] = reason
        self._assert_image_optional(image_url)
        self._assert_live_url(evidence_url)
        self.appeal_url[covenant_id] = evidence_url
        self.appeal_image_url[covenant_id] = image_url
        self.appeal_deadline[covenant_id] = self._now() + self.challenge_window
        self.state[covenant_id] = PENDING
        self.challenge_url[covenant_id] = evidence_url
        self.challenge_image_url[covenant_id] = image_url
        self.reason[covenant_id] = reason
        self.challenge_deadline[covenant_id] = self.appeal_deadline[covenant_id]
        self.round[covenant_id] = self.round[covenant_id] + u256(1)
        self._audit(covenant_id, "APPEAL_OPENED", gl.message.sender_address, reason)

    @gl.public.write
    def refresh_live_source(self, covenant_id: u256, live_url: str) -> None:
        """Change the monitored URL only while active and only by the publisher."""
        self._active(covenant_id)
        self._publisher(covenant_id)
        self._text(live_url, "live url")
        self._assert_live_url(live_url)
        self.live_url[covenant_id] = live_url
        self.source_version[covenant_id] = self.source_version[covenant_id] + u256(1)
        self._audit(covenant_id, "SOURCE_REFRESHED", gl.message.sender_address, "monitor URL updated")

    @gl.public.write
    def update_baseline_reference(self, covenant_id: u256, baseline_url: str, image_url: str) -> None:
        """Replace baseline evidence only before any challenge has started."""
        self._active(covenant_id)
        self._publisher(covenant_id)
        if self.round[covenant_id] != u256(0):
            raise gl.vm.UserError("baseline is immutable after challenge")
        self._text(baseline_url, "baseline url")
        self._assert_baseline_url(baseline_url)
        self._assert_image_optional(image_url)
        self.baseline_url[covenant_id] = baseline_url
        self.baseline_image_url[covenant_id] = image_url
        self.visual_required[covenant_id] = image_url != ""
        self.source_version[covenant_id] = self.source_version[covenant_id] + u256(1)
        self._audit(covenant_id, "BASELINE_UPDATED", gl.message.sender_address, "baseline reference changed")

    @gl.public.write.payable
    def challenge(self, covenant_id: u256, reason: str, evidence_url: str, image_url: str) -> None:
        self._active(covenant_id)
        self._text(reason,"reason")
        self._assert_live_url(evidence_url)
        self._assert_image_optional(image_url)
        if gl.message.value<self.minimum_bond: raise gl.vm.UserError("challenge bond below minimum")
        if gl.message.sender_address==self.publisher[covenant_id]: raise gl.vm.UserError("publisher cannot challenge")
        self.challenger[covenant_id]=gl.message.sender_address
        self.reason[covenant_id]=reason
        self.challenge_url[covenant_id]=evidence_url
        self.challenge_image_url[covenant_id]=image_url
        self.challenger_bond[covenant_id]=gl.message.value
        self.escrow[covenant_id]=self.escrow[covenant_id]+gl.message.value
        self.state[covenant_id]=PENDING
        self.challenged_at[covenant_id]=self._now()
        self.challenge_deadline[covenant_id]=self._now()+self.challenge_window
        self.round[covenant_id]=self.round[covenant_id]+u256(1)
        self.note[covenant_id]="challenge pending"
        self._audit(covenant_id,"CHALLENGE_OPENED",gl.message.sender_address,"semantic review requested")

    @gl.public.write
    def verify(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        if self.state[covenant_id]!=PENDING: raise gl.vm.UserError("pending challenge required")
        if self._now()>self.challenge_deadline[covenant_id]: raise gl.vm.UserError("challenge timed out")
        live=self.live_url[covenant_id]
        base=self.baseline_url[covenant_id]
        base_image=self.baseline_image_url[covenant_id]
        extra=self.challenge_url[covenant_id]
        extra_image=self.challenge_image_url[covenant_id]
        statement=self.statement[covenant_id]
        topics=self.topics[covenant_id]
        reason=self.reason[covenant_id]
        def leader_fn(): return self._evidence(live,base,base_image,extra,extra_image,statement,topics,reason)
        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result,gl.vm.Return): return False
            mine=self._evidence(live,base,base_image,extra,extra_image,statement,topics,reason)
            theirs=leader_result.calldata
            return mine["outcome"]==theirs["outcome"] and mine["impact"]==theirs["impact"] and mine["confidence"]==theirs["confidence"] and mine["mask"]==theirs["mask"]
        record=gl.vm.run_nondet_unsafe(leader_fn,validator_fn)
        record=self._normalize_record(record)
        final=self._derive_for_covenant(covenant_id,record)
        self.verdict[covenant_id]=final
        self.impact[covenant_id]=record["impact"]
        self.confidence[covenant_id]=record["confidence"]
        self.topic_mask[covenant_id]=record["mask"]
        self.checked_at[covenant_id]=self._now()
        if final==PRESERVED:
            self.state[covenant_id]=ACTIVE
            self.appeal_deadline[covenant_id]=u256(0)
        else:
            self.state[covenant_id]=RESOLVED
        if final==UNVERIFIABLE:
            self.recovery_deadline[covenant_id]=self._now()+self.recovery_window
            self.note[covenant_id]="unverifiable; recovery window"
        elif final==PRESERVED: self.note[covenant_id]="preserved"
        else: self.note[covenant_id]="adverse verdict"
        self._audit(covenant_id,"VERIFIED",gl.message.sender_address,self._verdict_name(final))
        return final

    def _evidence(self, live: str, base: str, base_image: str, extra: str, extra_image: str, statement: str, topics: str, reason: str):
        """Web fetch, rendered access and visual analysis
        only categories leave it."""
        live_text=gl.nondet.web.render(live,mode="text")
        base_text=gl.nondet.web.render(base,mode="text")
        images=[gl.nondet.web.render(live,mode="screenshot")]
        if base_image!="": images.append(gl.nondet.web.render(base_image,mode="screenshot"))
        if extra_image!="": images.append(gl.nondet.web.render(extra_image,mode="screenshot"))
        extra_text=""
        if extra!="": extra_text=gl.nondet.web.render(extra,mode="text")
        prompt=("Classify only material covenant meaning. Return JSON outcome "
                "PRESERVED|MATERIAL_CHANGE|REMOVED|UNVERIFIABLE; impact "
                "NONE|MINOR|MATERIAL|CRITICAL; confidence LOW|MEDIUM|HIGH; "
                "mask one of 0,1,2,3,4,7,8,15,16,31,32,63,64,127,128,255. "
                "Ignore wording/layout/timestamps. Statement: "+statement+" Topics: "+topics+" Challenge: "+reason+" Baseline: "+base_text[:10000]+" Current: "+live_text[:10000]+" Extra: "+extra_text[:4000])
        result=gl.nondet.exec_prompt(prompt,images=images,response_format="json")
        return {"outcome":self._outcome(str(result.get("outcome","UNVERIFIABLE"))),"impact":self._impact(str(result.get("impact","NONE"))),"confidence":self._confidence(str(result.get("confidence","LOW"))),"mask":self._mask(str(result.get("mask","0")))}

    def _derive(self,r) -> u256:
        if r["outcome"]==REMOVED: return REMOVED
        if r["outcome"]==CHANGED: return CHANGED
        if r["outcome"]==PRESERVED and r["confidence"]>=MEDIUM: return PRESERVED
        if r["outcome"]==PRESERVED and r["impact"]==NO_IMPACT and r["mask"]==u256(0): return PRESERVED
        return UNVERIFIABLE

    def _derive_for_covenant(self, covenant_id: u256, record) -> u256:
        """Apply covenant-specific policy after validators agree on categories."""
        if record["confidence"] < self.minimum_confidence[covenant_id]:
            return UNVERIFIABLE
        if record["impact"] > self.permitted_impact[covenant_id]:
            return UNVERIFIABLE
        if self.visual_required[covenant_id] and self.baseline_image_url[covenant_id] == "":
            return UNVERIFIABLE
        if not self.fallback_allowed[covenant_id] and record["outcome"] == UNVERIFIABLE:
            return UNVERIFIABLE
        return self._derive(record)

    def _verdict_name(self, verdict: u256) -> str:
        if verdict == PRESERVED:
            return "PRESERVED"
        if verdict == CHANGED:
            return "MATERIAL_CHANGE"
        if verdict == REMOVED:
            return "REMOVED"
        if verdict == UNVERIFIABLE:
            return "UNVERIFIABLE"
        if verdict == CANCELLED:
            return "CANCELLED"
        return "OTHER"

    @gl.public.write
    def claim_adverse(self,covenant_id:u256)->None:
        self._known(covenant_id)
        self._beneficiary(covenant_id)
        if self.verdict[covenant_id]!=CHANGED and self.verdict[covenant_id]!=REMOVED: raise gl.vm.UserError("adverse verdict required")
        if self.appeal_deadline[covenant_id] != u256(0) and self._deadline_is_open(self.appeal_deadline[covenant_id]): raise gl.vm.UserError("appeal window still open")
        self._audit(covenant_id,"CLAIM_REQUESTED",gl.message.sender_address,"beneficiary claimed adverse verdict")
        self._send_gen(covenant_id,self.beneficiary[covenant_id],self.publisher_bond[covenant_id],"adverse settlement")
        if self.challenger_bond[covenant_id] > u256(0): self._send_gen(covenant_id,self.challenger[covenant_id],self.challenger_bond[covenant_id],"challenge bond returned")

    @gl.public.write
    def claim_uncontested_expiry(self,covenant_id:u256)->None:
        self._known(covenant_id); self._publisher(covenant_id)
        if self.state[covenant_id]!=ACTIVE or self.round[covenant_id]!=u256(0) or not self._expiry_has_elapsed(covenant_id): raise gl.vm.UserError("uncontested expiry unavailable")
        self.verdict[covenant_id]=EXPIRED
        self._audit(covenant_id,"UNCONTESTED_EXPIRY",gl.message.sender_address,"normal expiry settlement")
        self._send_gen(covenant_id,self.publisher[covenant_id],self.publisher_bond[covenant_id],"uncontested expiry")

    @gl.public.write
    def claim_preserved_expiry(self,covenant_id:u256)->None:
        self._known(covenant_id)
        self._publisher(covenant_id)
        if self.verdict[covenant_id]!=PRESERVED or self._now()<self.expires_at[covenant_id]: raise gl.vm.UserError("preserved expiry required")
        self.verdict[covenant_id]=EXPIRED
        self._audit(covenant_id,"CLAIM_REQUESTED",gl.message.sender_address,"publisher claimed preserved expiry")
        self._send_gen(covenant_id,self.publisher[covenant_id],self.escrow[covenant_id],"preserved expiry")

    @gl.public.write
    def recover_unverifiable(self,covenant_id:u256)->None:
        self._known(covenant_id)
        if self.verdict[covenant_id]!=UNVERIFIABLE or self._now()<self.recovery_deadline[covenant_id]: raise gl.vm.UserError("unverifiable recovery unavailable")
        if gl.message.sender_address!=self.publisher[covenant_id] and gl.message.sender_address!=self.beneficiary[covenant_id] and gl.message.sender_address!=self.challenger[covenant_id]: raise gl.vm.UserError("party only")
        self._audit(covenant_id,"RECOVERY_REQUESTED",gl.message.sender_address,"unverifiable recovery")
        self._send_gen(covenant_id,self.publisher[covenant_id],self.escrow[covenant_id],"unverifiable recovery")

    @gl.public.write
    def recover_timed_out_challenge(self,covenant_id:u256)->None:
        self._known(covenant_id)
        self._publisher(covenant_id)
        if self.state[covenant_id]!=PENDING or self._now()<=self.challenge_deadline[covenant_id]: raise gl.vm.UserError("timed out pending challenge required")
        self.verdict[covenant_id]=UNVERIFIABLE
        self.state[covenant_id]=ACTIVE
        self._audit(covenant_id,"TIMEOUT_RECOVERY",gl.message.sender_address,"review round expired; covenant remains monitorable")
        self._send_gen(covenant_id,self.publisher[covenant_id],self.publisher_bond[covenant_id],"challenge timeout")
        if self.challenger_bond[covenant_id] > u256(0): self._send_gen(covenant_id,self.challenger[covenant_id],self.challenger_bond[covenant_id],"challenge bond returned")

    @gl.public.write
    def cancel_before_challenge(self,covenant_id:u256,reason:str)->None:
        self._active(covenant_id)
        self._publisher(covenant_id)
        self._text(reason,"reason")
        self.verdict[covenant_id]=CANCELLED
        self.state[covenant_id]=CLOSED
        self._audit(covenant_id,"CANCELLED",gl.message.sender_address,reason)
        self._send_gen(covenant_id,self.publisher[covenant_id],self.escrow[covenant_id],"cancelled: "+reason)

    def _send_gen(self,covenant_id:u256,recipient:Address,amount:u256,note:str)->None:
        """The only transfer emission: zero ledger and mark paid before emit."""
        if self.paid[covenant_id]: raise gl.vm.UserError("already paid")
        if amount==u256(0) or amount>self.escrow[covenant_id]: raise gl.vm.UserError("invalid payout")
        self.escrow[covenant_id]=self.escrow[covenant_id]-amount
        if amount<=self.publisher_bond[covenant_id]: self.publisher_bond[covenant_id]=self.publisher_bond[covenant_id]-amount
        elif amount<=self.challenger_bond[covenant_id]: self.challenger_bond[covenant_id]=self.challenger_bond[covenant_id]-amount
        self.paid[covenant_id]=self.escrow[covenant_id]==u256(0)
        self.paid_to[covenant_id]=recipient
        self.paid_amount[covenant_id]=self.paid_amount[covenant_id]+amount
        if self.paid[covenant_id]: self.state[covenant_id]=CLOSED
        self.note[covenant_id]=note
        self._audit(covenant_id,"TRANSFER_EMITTED",recipient,note)
        _Recipient(recipient).emit_transfer(value=amount,on="finalized")

    @gl.public.view
    def get_status(self,covenant_id:u256)->tuple[u256,u256,u256,u256,u256]:
        self._known(covenant_id)
        return (self.state[covenant_id],self.verdict[covenant_id],self.impact[covenant_id],self.confidence[covenant_id],self.escrow[covenant_id])
    @gl.public.view
    def get_evidence(self,covenant_id:u256)->tuple[str,str,str,str,str]:
        self._known(covenant_id)
        return (self.live_url[covenant_id],self.baseline_url[covenant_id],self.baseline_image_url[covenant_id],self.challenge_url[covenant_id],self.challenge_image_url[covenant_id])
    @gl.public.view
    def get_parties(self,covenant_id:u256)->tuple[Address,Address,Address]:
        self._known(covenant_id)
        return (self.publisher[covenant_id],self.beneficiary[covenant_id],self.challenger[covenant_id])
    @gl.public.view
    def get_payout(self,covenant_id:u256)->tuple[bool,Address,u256,str]:
        self._known(covenant_id)
        if not self.paid[covenant_id]:
            return (False,self.publisher[covenant_id],u256(0),self.note[covenant_id])
        return (self.paid[covenant_id],self.paid_to[covenant_id],self.paid_amount[covenant_id],self.note[covenant_id])

    @gl.public.view
    def get_identity(self, covenant_id: u256) -> tuple[str, str, str]:
        """Return label, promise statement and protected-topic declaration."""
        self._known(covenant_id)
        return (self.label[covenant_id], self.statement[covenant_id], self.topics[covenant_id])

    @gl.public.view
    def get_policy(self, covenant_id: u256) -> tuple[u256, u256, bool, bool]:
        """Return thresholds used by deterministic verdict derivation."""
        self._known(covenant_id)
        return (
            self.minimum_confidence[covenant_id],
            self.permitted_impact[covenant_id],
            self.visual_required[covenant_id],
            self.fallback_allowed[covenant_id],
        )

    @gl.public.view
    def get_settlement_policy(self, covenant_id: u256) -> tuple[u256, u256, u256]:
        self._known(covenant_id)
        return (
            self.settlement_publisher_bps[covenant_id],
            self.settlement_beneficiary_bps[covenant_id],
            self.settlement_challenger_bps[covenant_id],
        )

    @gl.public.view
    def get_deadlines(self, covenant_id: u256) -> tuple[u256, u256, u256, u256]:
        self._known(covenant_id)
        return (
            self.expires_at[covenant_id],
            self.challenge_deadline[covenant_id],
            self.recovery_deadline[covenant_id],
            self.appeal_deadline[covenant_id],
        )

    @gl.public.view
    def get_round_metadata(self, covenant_id: u256) -> tuple[u256, u256, u256, u256]:
        self._known(covenant_id)
        return (
            self.round[covenant_id],
            self.evidence_count[covenant_id],
            self.appeal_count[covenant_id],
            self.source_version[covenant_id],
        )

    @gl.public.view
    def get_latest_challenge(self, covenant_id: u256) -> tuple[str, str, str, Address]:
        self._known(covenant_id)
        return (
            self.reason[covenant_id],
            self.challenge_url[covenant_id],
            self.challenge_image_url[covenant_id],
            self.challenger[covenant_id],
        )

    @gl.public.view
    def get_latest_appeal(self, covenant_id: u256) -> tuple[str, str, str]:
        self._known(covenant_id)
        return (
            self.appeal_reason[covenant_id],
            self.appeal_url[covenant_id],
            self.appeal_image_url[covenant_id],
        )

    @gl.public.view
    def get_evidence_reference(self, covenant_id: u256, evidence_number: u256) -> tuple[str, str, str, u256]:
        self._known(covenant_id)
        if evidence_number == u256(0) or evidence_number > self.evidence_count[covenant_id]:
            raise gl.vm.UserError("unknown evidence reference")
        key = self._evidence_key_for(evidence_number, covenant_id)
        return (
            self.evidence_kind[key],
            self.evidence_url[key],
            self.evidence_digest[key],
            self.evidence_submitted_at[key],
        )

    @gl.public.view
    def get_audit_entry(self, covenant_id: u256, audit_number: u256) -> tuple[str, Address, u256, str]:
        self._known(covenant_id)
        if audit_number == u256(0) or audit_number > self.audit_count[covenant_id]:
            raise gl.vm.UserError("unknown audit entry")
        key = self._audit_key_for(audit_number, covenant_id)
        return (
            self.audit_action[key],
            self.audit_actor[key],
            self.audit_time[key],
            self.audit_note[key],
        )

    @gl.public.view
    def get_audit_count(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        return self.audit_count[covenant_id]

    @gl.public.view
    def get_evidence_count(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        return self.evidence_count[covenant_id]

    @gl.public.view
    def get_appeal_count(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        return self.appeal_count[covenant_id]

    @gl.public.view
    def get_source_version(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        return self.source_version[covenant_id]

    @gl.public.view
    def get_protocol_config(self) -> tuple[bool, u256, u256, u256]:
        return (self.paused, self.minimum_bond, self.challenge_window, self.recovery_window)

    @gl.public.view
    def is_claimable(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        if self.paid[covenant_id]:
            return False
        if self.verdict[covenant_id] == CHANGED or self.verdict[covenant_id] == REMOVED:
            return True
        if self.verdict[covenant_id] == PRESERVED and self._now() >= self.expires_at[covenant_id]:
            return True
        if self.verdict[covenant_id] == UNVERIFIABLE and self._now() >= self.recovery_deadline[covenant_id]:
            return True
        return False

    @gl.public.view
    def is_challenge_open(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == PENDING and self._now() <= self.challenge_deadline[covenant_id]

    @gl.public.view
    def is_expired(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self._now() >= self.expires_at[covenant_id]

    def _audit(self, covenant_id: u256, action: str, actor: Address, note: str) -> None:
        """Append an immutable, queryable lifecycle record.

        The record key is namespaced by covenant. Audit entries never influence
        consensus and never contain raw web content. They exist for builders,
        reviewers, and Explorer users who need to reconstruct why a ledger moved.
        """
        next_number = self.audit_count[covenant_id] + u256(1)
        self.audit_count[covenant_id] = next_number
        if next_number > MAX_AUDIT_RECORDS: raise gl.vm.UserError("audit limit reached")
        key = self._audit_key_for(next_number, covenant_id)
        self.audit_action[key] = action
        self.audit_actor[key] = actor
        self.audit_time[key] = self._now()
        self.audit_note[key] = note

    def _settlement_split_is_safe(self, covenant_id: u256) -> bool:
        """Check that a split cannot create or destroy escrow value."""
        self._known(covenant_id)
        return self._basis_points_are_valid(covenant_id)

    def _challenge_bond_is_recorded(self, covenant_id: u256) -> bool:
        """The challenger bond must be included in the same escrow ledger."""
        self._known(covenant_id)
        return self.challenger_bond[covenant_id] <= self.escrow[covenant_id]

    def _round_is_monotonic(self, covenant_id: u256, previous: u256) -> bool:
        """Rounds can only increase, preventing replay of an old evidence result."""
        self._known(covenant_id)
        return self.round[covenant_id] >= previous

    def _source_version_is_monotonic(self, covenant_id: u256, previous: u256) -> bool:
        """A source update is metadata and must never roll the version backwards."""
        self._known(covenant_id)
        return self.source_version[covenant_id] >= previous

    def _audit_is_append_only(self, covenant_id: u256, previous: u256) -> bool:
        """Audit storage is append-only because entries have sequence keys."""
        self._known(covenant_id)
        return self.audit_count[covenant_id] >= previous

    def _evidence_is_append_only(self, covenant_id: u256, previous: u256) -> bool:
        """Evidence references are never deleted or overwritten by this primitive."""
        self._known(covenant_id)
        return self.evidence_count[covenant_id] >= previous

    def _claim_requires_final_verdict(self, covenant_id: u256) -> bool:
        """A claim may only follow a terminal classification or timeout rule."""
        self._known(covenant_id)
        return self._outcome_is_terminal(self.verdict[covenant_id])

    def _claim_has_no_external_side_effect(self, covenant_id: u256) -> bool:
        """The ledger flag is set before the transfer message is emitted."""
        self._known(covenant_id)
        return self.paid[covenant_id] or self.escrow[covenant_id] == u256(0)

    def _record_has_no_raw_evidence(self, record) -> bool:
        """Consensus records are four scalar fields, never HTML or model prose."""
        return self._record_is_canonical(record)

    def _record_has_known_outcome(self, record) -> bool:
        return record["outcome"] == PRESERVED or record["outcome"] == CHANGED or record["outcome"] == REMOVED or record["outcome"] == UNVERIFIABLE

    def _record_has_known_impact(self, record) -> bool:
        return record["impact"] == NO_IMPACT or record["impact"] == MINOR or record["impact"] == MATERIAL or record["impact"] == CRITICAL

    def _record_has_known_confidence(self, record) -> bool:
        return record["confidence"] == LOW or record["confidence"] == MEDIUM or record["confidence"] == HIGH

    def _record_is_safe_to_store(self, record) -> bool:
        return self._record_has_known_outcome(record) and self._record_has_known_impact(record) and self._record_has_known_confidence(record) and self._topic_mask_is_bounded(record["mask"])

    def _covenant_is_recoverable(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        if self.paid[covenant_id]:
            return False
        if self.verdict[covenant_id] == UNVERIFIABLE:
            return self._deadline_has_elapsed(self.recovery_deadline[covenant_id])
        return self.verdict[covenant_id] == PRESERVED and self._expiry_has_elapsed(covenant_id)

    def _covenant_is_settled(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.paid[covenant_id] and self.escrow[covenant_id] == u256(0)

    def _covenant_has_active_challenge(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == PENDING and self._deadline_is_open(self.challenge_deadline[covenant_id])

    def _covenant_has_expired_challenge(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == PENDING and self._deadline_has_elapsed(self.challenge_deadline[covenant_id])

    def _covenant_can_be_cancelled(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == ACTIVE and not self.paid[covenant_id]

    def _covenant_can_be_reverified(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == RESOLVED and not self.paid[covenant_id] and self.appeal_count[covenant_id] < u256(2)

    def _covenant_party(self, covenant_id: u256, actor: Address) -> bool:
        self._known(covenant_id)
        return actor == self.publisher[covenant_id] or actor == self.beneficiary[covenant_id] or actor == self.challenger[covenant_id]

    def _covenant_is_owner(self, actor: Address) -> bool:
        return actor == self.owner

    def _verdict_is_preserved(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.verdict[covenant_id] == PRESERVED

    def _verdict_is_unverifiable(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.verdict[covenant_id] == UNVERIFIABLE

    def _verdict_is_adverse(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self._outcome_is_adverse(self.verdict[covenant_id])

    def _assert_live_url(self, value: str) -> None:
        self._text(value, "live url")
        if not value.startswith("https://") or "://" not in value or "@" in value: raise gl.vm.UserError("HTTPS URL required")

    def _assert_baseline_url(self, value: str) -> None:
        self._text(value, "baseline url")
        if not value.startswith("https://") or "://" not in value or "@" in value: raise gl.vm.UserError("HTTPS URL required")

    def _assert_image_optional(self, value: str) -> None:
        if value != "":
            self._text(value, "image url")

    def _assert_digest(self, value: str) -> None:
        self._text(value, "digest")
        if len(value)!=64: raise gl.vm.UserError("digest must be 64 hex characters")
        for ch in value.lower():
            if ch not in "0123456789abcdef": raise gl.vm.UserError("digest must be hex")

    def _assert_round_is_open(self, covenant_id: u256) -> None:
        if not self._state_allows_evidence(covenant_id):
            raise gl.vm.UserError("evidence round is closed")

    def _assert_no_active_appeal(self, covenant_id: u256) -> None:
        if self.appeal_deadline[covenant_id] != u256(0) and self._deadline_is_open(self.appeal_deadline[covenant_id]):
            raise gl.vm.UserError("appeal already open")

    def _assert_challenge_deadline(self, covenant_id: u256) -> None:
        if not self._deadline_is_open(self.challenge_deadline[covenant_id]):
            raise gl.vm.UserError("challenge deadline closed")

    def _assert_recovery_deadline(self, covenant_id: u256) -> None:
        if not self._deadline_has_elapsed(self.recovery_deadline[covenant_id]):
            raise gl.vm.UserError("recovery deadline not elapsed")

    def _assert_expiry_deadline(self, covenant_id: u256) -> None:
        if not self._expiry_has_elapsed(covenant_id):
            raise gl.vm.UserError("expiry deadline not elapsed")

    def _assert_transferable(self, covenant_id: u256) -> None:
        self._require_unpaid(covenant_id)
        if not self._escrow_is_positive(covenant_id):
            raise gl.vm.UserError("empty escrow")

    def _assert_recipient(self, covenant_id: u256, recipient: Address) -> None:
        if not self._payout_recipient_is_party(covenant_id, recipient):
            raise gl.vm.UserError("recipient is not a covenant party")

    def _assert_protocol_live(self) -> None:
        if self.paused:
            raise gl.vm.UserError("protocol paused")

    def _assert_positive_bond(self, amount: u256) -> None:
        if amount == u256(0):
            raise gl.vm.UserError("bond must be positive")

    def _assert_future_timestamp(self, timestamp: u256) -> None:
        if timestamp <= self._now():
            raise gl.vm.UserError("timestamp must be in the future")

    def _assert_nonzero_id(self, covenant_id: u256) -> None:
        if covenant_id == u256(0):
            raise gl.vm.UserError("identifier must be nonzero")

    def _assert_known_party(self, covenant_id: u256, actor: Address) -> None:
        if not self._covenant_party(covenant_id, actor):
            raise gl.vm.UserError("unknown covenant party")

    def _outcome(self,x:str)->u256:
        if x=="PRESERVED": return PRESERVED
        if x=="MATERIAL_CHANGE": return CHANGED
        if x=="REMOVED": return REMOVED
        return UNVERIFIABLE

    # ------------------------------------------------------------------
    # Deterministic policy helpers. These are intentionally kept separate
    # from the nondeterministic evidence block. Every one of these functions
    # accepts canonical scalar values and can therefore be replayed by every
    # validator without a web call, model call, or host dependency.
    # ------------------------------------------------------------------

    def _confidence_is_acceptable(self, covenant_id: u256, value: u256) -> bool:
        self._known(covenant_id)
        return value >= self.minimum_confidence[covenant_id]

    def _impact_is_permitted(self, covenant_id: u256, value: u256) -> bool:
        self._known(covenant_id)
        return value <= self.permitted_impact[covenant_id]

    def _visual_policy_is_satisfied(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        if not self.visual_required[covenant_id]:
            return True
        return self.baseline_image_url[covenant_id] != ""

    def _fallback_policy_is_satisfied(self, covenant_id: u256, value: u256) -> bool:
        self._known(covenant_id)
        if value != UNVERIFIABLE:
            return True
        return self.fallback_allowed[covenant_id]

    def _policy_accepts_record(self, covenant_id: u256, record) -> bool:
        if not self._confidence_is_acceptable(covenant_id, record["confidence"]):
            return False
        if not self._impact_is_permitted(covenant_id, record["impact"]):
            return False
        if not self._visual_policy_is_satisfied(covenant_id):
            return False
        return self._fallback_policy_is_satisfied(covenant_id, record["outcome"])

    def _topic_mask_is_bounded(self, value: u256) -> bool:
        return value <= TOPIC_MASK_MAX

    def _record_is_canonical(self, record) -> bool:
        if record["outcome"] < PRESERVED or record["outcome"] > UNVERIFIABLE:
            return False
        if record["impact"] > CRITICAL:
            return False
        if record["confidence"] > HIGH:
            return False
        return self._topic_mask_is_bounded(record["mask"])

    def _record_or_safe_fallback(self, record):
        if not self._record_is_canonical(record):
            return {"outcome": UNVERIFIABLE, "impact": NO_IMPACT, "confidence": LOW, "mask": u256(0)}
        return record

    def _outcome_is_adverse(self, value: u256) -> bool:
        return value == CHANGED or value == REMOVED

    def _outcome_is_non_adverse(self, value: u256) -> bool:
        return value == PRESERVED or value == UNVERIFIABLE

    def _outcome_is_terminal(self, value: u256) -> bool:
        return value == PRESERVED or value == CHANGED or value == REMOVED or value == UNVERIFIABLE or value == CANCELLED or value == EXPIRED

    def _state_is_open(self, value: u256) -> bool:
        return value == ACTIVE or value == PENDING

    def _state_is_closed(self, value: u256) -> bool:
        return value == RESOLVED or value == CLOSED

    def _state_allows_metadata(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == ACTIVE

    def _state_allows_evidence(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == ACTIVE or self.state[covenant_id] == PENDING

    def _state_allows_appeal(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == RESOLVED and not self.paid[covenant_id]

    def _deadline_has_elapsed(self, deadline: u256) -> bool:
        return deadline != u256(0) and self._now() > deadline

    def _deadline_is_open(self, deadline: u256) -> bool:
        return deadline != u256(0) and self._now() <= deadline

    def _expiry_has_elapsed(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self._now() >= self.expires_at[covenant_id]

    def _expiry_is_open(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self._now() < self.expires_at[covenant_id]

    def _escrow_is_positive(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.escrow[covenant_id] > u256(0)

    def _escrow_matches_components(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.escrow[covenant_id] == self.publisher_bond[covenant_id] + self.beneficiary_bond[covenant_id] + self.challenger_bond[covenant_id]

    def _basis_points_are_valid(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.settlement_publisher_bps[covenant_id] + self.settlement_beneficiary_bps[covenant_id] + self.settlement_challenger_bps[covenant_id] == u256(10000)

    def _basis_points_amount(self, amount: u256, bps: u256) -> u256:
        if bps > u256(10000):
            raise gl.vm.UserError("basis points out of range")
        return amount * bps // u256(10000)

    def _remaining_basis_points_amount(self, amount: u256, first: u256, second: u256) -> u256:
        first_amount = self._basis_points_amount(amount, first)
        second_amount = self._basis_points_amount(amount, second)
        return amount - first_amount - second_amount

    def _evidence_key(self, covenant_id: u256, number: u256) -> u256:
        self._known(covenant_id)
        if number == u256(0) or number > self.evidence_count[covenant_id]:
            raise gl.vm.UserError("evidence number out of range")
        return self._evidence_key_for(number, covenant_id)

    def _evidence_key_for(self, number: u256, covenant_id: u256) -> u256:
        return (covenant_id << u256(32)) | number

    def _audit_key(self, covenant_id: u256, number: u256) -> u256:
        self._known(covenant_id)
        if number == u256(0) or number > self.audit_count[covenant_id]:
            raise gl.vm.UserError("audit number out of range")
        return self._audit_key_for(number, covenant_id)

    def _audit_key_for(self, number: u256, covenant_id: u256) -> u256:
        return (covenant_id << u256(32)) | number

    def _appeal_is_available(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self._state_allows_appeal(covenant_id) and self.appeal_count[covenant_id] < u256(2)

    def _challenge_is_available(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return self.state[covenant_id] == ACTIVE and self._expiry_is_open(covenant_id)

    def _publisher_can_update_source(self, covenant_id: u256) -> bool:
        return self._state_allows_metadata(covenant_id) and gl.message.sender_address == self.publisher[covenant_id]

    def _party_can_submit_evidence(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        sender = gl.message.sender_address
        return sender == self.publisher[covenant_id] or sender == self.beneficiary[covenant_id] or sender == self.challenger[covenant_id]

    def _party_can_request_recovery(self, covenant_id: u256) -> bool:
        return self._party_can_submit_evidence(covenant_id)

    def _payout_is_unclaimed(self, covenant_id: u256) -> bool:
        self._known(covenant_id)
        return not self.paid[covenant_id] and self._escrow_is_positive(covenant_id)

    def _payout_recipient_is_party(self, covenant_id: u256, recipient: Address) -> bool:
        self._known(covenant_id)
        return recipient == self.publisher[covenant_id] or recipient == self.beneficiary[covenant_id] or recipient == self.challenger[covenant_id]

    def _safe_payout_amount(self, covenant_id: u256) -> u256:
        self._known(covenant_id)
        if not self._escrow_matches_components(covenant_id):
            raise gl.vm.UserError("escrow component mismatch")
        return self.escrow[covenant_id]

    def _set_verdict_metadata(self, covenant_id: u256, record, verdict: u256) -> None:
        self._known(covenant_id)
        self.verdict[covenant_id] = verdict
        self.impact[covenant_id] = record["impact"]
        self.confidence[covenant_id] = record["confidence"]
        self.topic_mask[covenant_id] = record["mask"]
        self.checked_at[covenant_id] = self._now()

    def _open_recovery_window(self, covenant_id: u256) -> None:
        self._known(covenant_id)
        self.recovery_deadline[covenant_id] = self._now() + self.recovery_window
        self.note[covenant_id] = "recovery window open"

    def _close_without_transfer(self, covenant_id: u256, verdict: u256, note: str) -> None:
        self._known(covenant_id)
        if self.paid[covenant_id]:
            raise gl.vm.UserError("already settled")
        self.verdict[covenant_id] = verdict
        self.state[covenant_id] = CLOSED
        self.note[covenant_id] = note

    def _require_open_state(self, covenant_id: u256) -> None:
        self._known(covenant_id)
        if not self._state_is_open(self.state[covenant_id]):
            raise gl.vm.UserError("covenant is not open")

    def _require_unpaid(self, covenant_id: u256) -> None:
        self._known(covenant_id)
        if self.paid[covenant_id]:
            raise gl.vm.UserError("covenant already paid")

    def _require_valid_policy(self, covenant_id: u256) -> None:
        self._known(covenant_id)
        if not self._basis_points_are_valid(covenant_id):
            raise gl.vm.UserError("invalid settlement policy")
        if self.minimum_confidence[covenant_id] > HIGH:
            raise gl.vm.UserError("invalid confidence policy")
        if self.permitted_impact[covenant_id] > CRITICAL:
            raise gl.vm.UserError("invalid impact policy")

    def _require_canonical_record(self, record) -> None:
        if not self._record_is_canonical(record):
            raise gl.vm.UserError("non-canonical evidence result")

    def _normalize_record(self, record):
        canonical = self._record_or_safe_fallback(record)
        self._require_canonical_record(canonical)
        return canonical
    def _impact(self,x:str)->u256:
        if x=="CRITICAL": return CRITICAL
        if x=="MATERIAL": return MATERIAL
        if x=="MINOR": return MINOR
        return NO_IMPACT
    def _confidence(self,x:str)->u256:
        if x=="HIGH": return HIGH
        if x=="MEDIUM": return MEDIUM
        return LOW
    def _mask(self,x:str)->u256:
        if x=="1": return u256(1)
        if x=="2": return u256(2)
        if x=="3": return u256(3)
        if x=="4": return u256(4)
        if x=="7": return u256(7)
        if x=="8": return u256(8)
        if x=="15": return u256(15)
        if x=="16": return u256(16)
        if x=="31": return u256(31)
        if x=="32": return u256(32)
        if x=="63": return u256(63)
        if x=="64": return u256(64)
        if x=="127": return u256(127)
        if x=="128": return u256(128)
        if x=="255": return u256(255)
        return u256(0)
    def _now(self)->u256: return u256(int(datetime.now(timezone.utc).timestamp()))
    def _owner(self)->None:
        if gl.message.sender_address!=self.owner: raise gl.vm.UserError("owner only")
    def _publisher(self,i:u256)->None:
        if gl.message.sender_address!=self.publisher[i]: raise gl.vm.UserError("publisher only")
    def _beneficiary(self,i:u256)->None:
        if gl.message.sender_address!=self.beneficiary[i]: raise gl.vm.UserError("beneficiary only")
    def _known(self,i:u256)->None:
        if i==u256(0) or i>self.count: raise gl.vm.UserError("unknown covenant")
    def _active(self,i:u256)->None:
        self._known(i)
        if self.state[i]!=ACTIVE or self._now()>=self.expires_at[i]: raise gl.vm.UserError("inactive or expired")
    def _text(self,x:str,name:str)->None:
        if x=="": raise gl.vm.UserError(name+" required")
        limit=MAX_DESCRIPTION_CHARS
        if name=="label": limit=MAX_LABEL_CHARS
        elif name=="statement": limit=MAX_STATEMENT_CHARS
        elif name=="topics": limit=MAX_TOPICS_CHARS
        elif "reason" in name: limit=MAX_REASON_CHARS
        elif "url" in name or "image" in name: limit=MAX_URL_CHARS
        if len(x)>limit: raise gl.vm.UserError(name+" too long")
