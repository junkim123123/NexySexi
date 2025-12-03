export type EmailType = "business" | "prosumer" | "free" | "disposable_or_risky";
export type EmailLocalPartType = "role_based" | "person_name" | "suspicious";

export interface EmailIntel {
  domain: string;
  emailType: EmailType;
  localPartType: EmailLocalPartType;
}

const FREE_EMAIL_DOMAINS = new Set<string>([
  "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
  "live.com", "msn.com", "icloud.com", "me.com", "mac.com",
  "protonmail.com", "proton.me", "mail.com", "gmx.com", "gmx.de",
  "yandex.com", "yandex.ru", "mail.ru",
  "qq.com", "163.com", "126.com", "sina.com",
  "zoho.com", "fastmail.com",
  "naver.com", "web.de", "libero.it", "orange.fr", "wanadoo.fr",
  // add more if needed
]);

const DISPOSABLE_DOMAINS = new Set<string>([
  "mailinator.com", "guerrillamail.com", "temp-mail.org",
  "10minutemail.com", "sharklasers.com", "grr.la",
  // extend from research if desired
]);

const ROLE_BASED_PREFIXES = [
  "info", "sales", "support", "admin", "contact", "help", "hr"
];

export function analyzeEmail(email: string): EmailIntel {
  const [localRaw, domainRaw] = email.toLowerCase().split("@");
  const local = (localRaw || "").trim();
  const domain = (domainRaw || "").trim();

  let emailType: EmailType = "prosumer";
  if (DISPOSABLE_DOMAINS.has(domain)) {
    emailType = "disposable_or_risky";
  } else if (FREE_EMAIL_DOMAINS.has(domain)) {
    emailType = "free";
  } else if (domain.length <= 4) {
    // extremely short domains are often prosumer/personal unless known brand
    emailType = "prosumer";
  } else {
    emailType = "business";
  }

  let localPartType: EmailLocalPartType = "person_name";
  const numericRun = (local.match(/\d{4,}/) || [])[0];
  const isRole = ROLE_BASED_PREFIXES.some((p) => local === p || local.startsWith(`${p}+`));

  if (isRole) {
    localPartType = "role_based";
  } else if (numericRun) {
    localPartType = "suspicious";
  } else if (local.length <= 2) {
    localPartType = "suspicious";
  } else {
    localPartType = "person_name";
  }

  return { domain, emailType, localPartType };
}