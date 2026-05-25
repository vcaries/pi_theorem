import { Check, Copy } from "lucide-react";
import { useState } from "react";

import { Katex } from "@/lib/Katex";
import type { PiGroupOut } from "@/types";

interface PiGroupCardProps {
  group: PiGroupOut;
  /** Stagger index used for a subtle entrance animation. */
  order: number;
}

/** A card displaying one dimensionless group with a copy-to-clipboard action. */
export function PiGroupCard({ group, order }: PiGroupCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(group.ascii);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard unavailable; ignore */
    }
  };

  return (
    <div
      className="card animate-fade-in-up flex items-center justify-between gap-4 px-5 py-4"
      style={{ animationDelay: `${order * 60}ms` }}
    >
      <div className="overflow-x-auto py-1">
        <Katex math={group.latex} display />
      </div>
      <button
        type="button"
        onClick={handleCopy}
        className="shrink-0 rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-brand-600 dark:hover:bg-slate-800"
        title={group.ascii}
        aria-label="Copy"
      >
        {copied ? <Check size={16} className="text-emerald-500" /> : <Copy size={16} />}
      </button>
    </div>
  );
}
