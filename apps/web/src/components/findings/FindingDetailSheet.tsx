import { X } from "lucide-react";
import type { Finding } from "../../features/findings/useFindings";
import { EvidenceStepper } from "./EvidenceStepper";

export function FindingDetailSheet({ finding, onClose }: { finding: Finding | null; onClose: () => void }) {
	if (!finding) return null;
	return <div className="sheet-backdrop" onClick={onClose}><aside className="finding-sheet" onClick={(event) => event.stopPropagation()}><button className="dialog-close" aria-label="Close finding" onClick={onClose}><X size={18} /></button><p className="eyebrow">Finding detail</p><h2>{finding.title}</h2><EvidenceStepper finding={finding} /></aside></div>;
}
