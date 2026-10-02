export const BASE: string;

export interface Problem { code: string; where: string; says: string; fix: string; retry_after?: number }

export class Merch1211Error extends Error {
  status: number;
  problems: Problem[];
}

export interface DesignSide {
  ok: boolean;
  prints_in: [number, number];
  dpi: number;
  px: [number, number];
  says: string;
  placement?: "chest" | "center";
}

export interface Design {
  design: string;
  /** The page where the person sees it, picks sizes and pays. Give them this. */
  url: string;
  mockup: { front: string | null; back: string | null };
  item: string;
  item_name: string;
  color: string;
  title: string;
  sides: { front?: DesignSide; back?: DesignSide };
  price: { usd: number; bigger_sizes_usd: Record<string, number>; shipping: string };
  problems: Problem[];
  expires: string | null;
}

export interface Upload { ok: true; upload: string; w: number; h: number; grade?: string; says?: string; preview?: string; expires_days?: number }

export interface Opts { base?: string }

export interface DesignInput extends Opts {
  item: string;
  imageUrl?: string;
  uploadId?: string;
  color?: string;
  side?: "front" | "back" | "both";
  front?: "chest" | "center";
  size?: string;
  backImageUrl?: string;
  backUploadId?: string;
  title?: string;
  ref?: string;
}

export function catalog(opts?: Opts): Promise<any>;
export function upload(file: Blob, opts?: Opts): Promise<Upload>;
export function createDesign(input: DesignInput): Promise<Design>;
export function getDesign(id: string, opts?: Opts): Promise<Design>;
export function makeLink(input: Omit<DesignInput, "uploadId" | "backImageUrl" | "backUploadId">): string;
