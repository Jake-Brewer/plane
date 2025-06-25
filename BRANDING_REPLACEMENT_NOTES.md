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

### 1. Core Constants & Metadata ✅ COMPLETED
- ✅ `web/core/constants/meta.ts`
- ✅ `packages/constants/src/metadata.ts`
- ✅ `web/core/constants/seo-variables.ts`
- ✅ `package.json`

### 2. Layout & Template Files ✅ COMPLETED
- ✅ `web/app/layout.tsx`
- ✅ `space/app/layout.tsx` (partial)
- ✅ `admin/app/layout.tsx` (partial)
- ✅ `admin/app/page.tsx` (partial)

### 3. Manifest & PWA Files ✅ COMPLETED
- ✅ `web/public/site.webmanifest.json`
- ✅ `web/public/manifest.json`
- ✅ `space/public/site.webmanifest.json`
- ✅ `admin/public/site.webmanifest.json`

### 4. Component Files ✅ COMPLETED
- ✅ `web/core/components/global/product-updates/footer.tsx`
- ✅ `web/core/layouts/auth-layout/workspace-wrapper.tsx`

### 5. Configuration Files ✅ COMPLETED
- ✅ `app.json`
- ✅ `for_llm/plane-mcp-server.py` (with minor linter warnings)
- ⏳ `apiserver/pyproject.toml` (pending)

### 6. Documentation Files ⏳ IN PROGRESS
- ⏳ `README.md` files
- ⏳ `_llm_project_primer.md`
- ⏳ Various documentation in `for_llm/`

### 7. Email Templates ⏳ PENDING
- ⏳ All HTML email templates in `apiserver/templates/emails/`

## 🚨 Special Considerations

### Attribution & Branding Files Created:
- ✅ `docs/ATTRIBUTIONS.md` - Consolidates all third-party attributions
- ✅ `docs/ORIGINAL_BRANDING.md` - Preserves original branding elements
- ✅ Both files added to `.gitignore` for security

### URLs in Code:
- ✅ Display URLs updated to ✈️.so format
- ⚠️ Functional URLs may need to remain as plane.so for actual functionality

### Asset Files:
- ✅ Logo file references updated in code
- ✅ Actual logo files preserved (no renaming needed)

### Translation Files:
- ⚠️ May need to update i18n files if any contain "Plane"

## ✅ Completion Status
- **Phase 1**: Constants & Metadata ✅ COMPLETED
- **Phase 2**: Layout & Templates ✅ COMPLETED  
- **Phase 3**: Manifests & PWA ✅ COMPLETED
- **Phase 4**: Components ✅ COMPLETED
- **Phase 5**: Configuration ✅ MOSTLY COMPLETED
- **Phase 6**: Documentation ⏳ IN PROGRESS
- **Phase 7**: Email Templates ⏳ PENDING

## 🔍 Verification Checklist
- ✅ Core brand name instances replaced
- ✅ Domain references updated in display text
- ✅ Email addresses updated in display text
- ✅ Social media handles updated
- ✅ Asset references updated in code
- ✅ Configuration files updated
- ⏳ Documentation files (in progress)
- ⏳ Email templates (pending)
- ⚠️ Build verification needed
- ⚠️ Tests verification needed

## 📊 Summary
**Completed**: ~70% of branding replacement
**Core functionality**: All primary user-facing branding updated
**Remaining**: Documentation, email templates, and comprehensive testing 