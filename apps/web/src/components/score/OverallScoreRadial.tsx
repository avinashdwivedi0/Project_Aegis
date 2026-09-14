export function OverallScoreRadial({ score }: { score: number | null }) {
	return <div className="score-panel"><span>Overall quality</span><strong>{score ?? "--"}</strong></div>;
}
