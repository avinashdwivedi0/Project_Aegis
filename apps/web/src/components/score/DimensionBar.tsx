export function DimensionBar({ label, score }: { label: string; score: number }) {
	return <div className="dimension-row"><span>{label.replace(/_/g, " ")}</span><div className="bar"><i style={{ width: `${score}%` }} /></div><strong>{score}</strong></div>;
}
