# 🔄 Branding Replacement Notes

## 📝 Overview
Systematic replacement of all "Plane" branding with emojis across the entire codebase.

## 🎯 Replacement Strategy

### Primary Brand Replacements:
- **"Plane"** → **"✈️"** (airplane emoji)
- **"plane"** → **"✈️"** 
- **"PLANE"** → **"✈️"**

### Domain & URL Replacements:
- **plane.so** → **✈️.so** 
- **app.plane.so** → **app.✈️.so**
- **docs.plane.so** → **docs.✈️.so**
- **go.plane.so** → **go.✈️.so**
- **sites.plane.so** → **sites.✈️.so**
- **prime.plane.so** → **prime.✈️.so**
- **telemetry.plane.so** → **telemetry.✈️.so**

### Email Replacements:
- **support@plane.so** → **support@✈️.so**
- **security@plane.so** → **security@✈️.so**
- **sales@plane.so** → **sales@✈️.so**
- **team@mailer.plane.so** → **team@mailer.✈️.so**

### Title & Description Replacements:
- **"Plane | Simple, extensible, open-source project management tool."** → **"✈️ | Simple, extensible, open-source project management tool."**
- **"Open-source project management tool to manage issues, sprints, and product roadmaps with peace of mind."** → **"Open-source project management tool to manage issues, sprints, and product roadmaps with peace of mind."** (keeping description as-is)

### Social Media:
- **@planepowers** → **@✈️powers**

### File & Asset Names:
- **plane-logos/** → **✈️-logos/**
- **plane-mobile-pwa.png** → **✈️-mobile-pwa.png**
- **plane-logo.svg** → **✈️-logo.svg**
- **PlaneLogo** → **✈️Logo**

### Repository & Package:
- **makeplane/plane** → **make✈️/✈️**
- **"name": "plane"** → **"name": "✈️"**

## 📋 Files to Update

### 1. Core Constants & Metadata
- [x] `web/core/constants/meta.ts`
- [x] `packages/constants/src/metadata.ts`
- [x] `web/core/constants/seo-variables.ts`
- [x] `package.json`

### 2. Layout & Template Files
- [x] `web/app/layout.tsx`
- [x] `space/app/layout.tsx`
- [x] `admin/app/layout.tsx`
- [x] `admin/app/page.tsx`

### 3. Manifest & PWA Files
- [x] `web/public/site.webmanifest.json`
- [x] `web/public/manifest.json`
- [x] `space/public/site.webmanifest.json`
- [x] `admin/public/site.webmanifest.json`

### 4. Component Files
- [x] `web/core/components/global/product-updates/footer.tsx`
- [x] `web/core/layouts/auth-layout/workspace-wrapper.tsx`

### 5. Configuration Files
- [x] `app.json`
- [x] `apiserver/pyproject.toml`

### 6. Documentation Files
- [x] `README.md` files
- [x] `_llm_project_primer.md`
- [x] Various documentation in `for_llm/`

### 7. Email Templates
- [x] All HTML email templates in `apiserver/templates/emails/`

## 🚨 Special Considerations

### URLs in Code:
- Need to be careful with actual functional URLs vs display text
- May need to keep some functional URLs working while changing display text

### Asset Files:
- Logo image files themselves don't need renaming (would break references)
- Only references in code need updating

### Translation Files:
- Need to update i18n files if any contain "Plane"

## ✅ Completion Status
- **Phase 1**: Constants & Metadata ✅
- **Phase 2**: Layout & Templates ✅  
- **Phase 3**: Manifests & PWA ✅
- **Phase 4**: Components ✅
- **Phase 5**: Configuration ✅
- **Phase 6**: Documentation ✅
- **Phase 7**: Email Templates ✅

## 🔍 Verification Checklist
- [ ] All brand name instances replaced
- [ ] All domain references updated
- [ ] All email addresses updated
- [ ] All social media handles updated
- [ ] All asset references updated
- [ ] All configuration files updated
- [ ] No broken references or imports
- [ ] Build still works
- [ ] Tests still pass 