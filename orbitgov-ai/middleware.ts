import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedRoutes = ["/dashboard", "/ai-assistant", "/subscription", "/admin"];

export function middleware(req: NextRequest) {
  if (!protectedRoutes.some((route) => req.nextUrl.pathname.startsWith(route))) {
    return NextResponse.next();
  }

  const hasSession = Boolean(req.cookies.get("orbitgov_session")?.value);
  if (hasSession) return NextResponse.next();

  const loginUrl = new URL("/login", req.url);
  loginUrl.searchParams.set("next", req.nextUrl.pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = { matcher: ["/dashboard/:path*", "/ai-assistant/:path*", "/subscription/:path*", "/admin/:path*"] };
