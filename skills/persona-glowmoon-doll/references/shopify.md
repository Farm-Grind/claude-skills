# Glowmoon Shopify — Operations Reference

Shopify operations reference for glowmoondoll.com.
Artist-run small store; prioritize simplicity, maintainability, and Isabel's
ability to manage content without coding.

## Contents
- § STORE CONTEXT
- § PART 1 — Shopify Architecture Fundamentals
- § PART 2 — Products and Variants
- § PART 3 — Collections and Navigation
- § PART 4 — Theme Editor (No-Code Changes)
- § PART 5 — Safe Code Editing Workflow
- § PART 6 — Metafields for Glowmoon-Specific Needs
- § PART 7 — Theme Migration: Debut → Dawn
- § PART 8 — Common Admin Tasks

---

## § STORE CONTEXT

| Field | Value |
|---|---|
| Store URL | glowmoondoll.com |
| Shopify account | boudi-doll.myshopify.com |
| Current theme | Debut (legacy — no new feature updates) |
| Target theme | Dawn (Online Store 2.0 — free, maintained by Shopify) |
| Currency | USD |
| Products | Resin BJDs (Boudi), vinyl dolls (Rune), accessories, full sets |
| Custom orders | Via email; faceup options, resin colors, special requests |

**Theme migration flag:** Debut receives no new Shopify feature updates.
Dawn is 35% faster, supports sections on every page (not just homepage),
enables metafields natively, and supports app blocks. Migration is a
significant one-time task — see PART 7 before doing any substantial Debut
customization.

---

## § PART 1 — Shopify Architecture Fundamentals

### Theme file structure (Online Store 2.0 / Dawn)

```
/templates/     → JSON templates per page type (product, collection, index...)
/sections/      → Modular, reusable content blocks; each has a {% schema %} block
/snippets/      → Small reusable code fragments (DRY principle)
/assets/        → CSS, JS, images
/config/        → Theme settings data and schema
/locales/       → Translation strings
```

Key principle: Sections are editable in the Theme Editor without code.
Snippets are code-only. JSON templates define which sections appear on each page.

### Liquid basics

| Syntax | Purpose |
|---|---|
| `{{ product.title }}` | Output dynamic data |
| `{% if %}...{% endif %}` | Conditional logic |
| `{% for %}...{% endfor %}` | Loops |
| `{% render 'snippet-name' %}` | Include a snippet (use `render`, not `include` — deprecated) |
| `{% schema %}...{% endschema %}` | Define Theme Editor settings for a section |

Safe editing rule: Always duplicate the active theme before making edits.
Work on the duplicate; publish only when tested.

---

## § PART 2 — Products and Variants

### Glowmoon product types and variant structure

| Product type | Typical variants | Notes |
|---|---|---|
| Resin BJD (Boudi) | Resin color, faceup option | Colors may look different on screen vs. in person — caveat in copy |
| Vinyl doll (Rune) | Style/outfit edition, faceup | Character-driven; each release has a name |
| Full set | May bundle doll + accessories | Separate SKU from blank doll |
| Accessories | Size, type | Sold separately |

Shopify variant limits: Up to 3 option types, up to 2,048 variants per product.
For Glowmoon's catalog this is not a concern, but avoid over-combining options.

### Faceup option setup (standard approach)

Faceup is an add-on/choice, not a separate product. Model as a variant option:
- Option name: "Faceup"
- Values: "No faceup (blank)", "Artist-choice faceup — dark brows", "Artist-choice faceup — light brows"
- For custom/unusual requests: direct to email in product description

Alternative for complex faceup logic: Use a product metafield
(`custom.faceup_note`) to store per-product faceup instructions that
display on the product page.

### When to use variants vs. metafields

| Use case | Use variants | Use metafields |
|---|---|---|
| Customer selects between options at purchase | Yes | — |
| Informational detail per variant (e.g., resin care notes) | — | Yes (variant metafield) |
| Informational detail per product (e.g., measurements) | — | Yes (product metafield) |
| Linking related dolls (color family, same character) | — | Yes (product reference list) |

### Creating a metafield definition

Admin → Settings → Custom Data → [resource] → Add definition
- Namespace: use `custom` for store-specific fields
- Key: descriptive snake_case (e.g., `resin_color_notes`, `faceup_instructions`)
- Display in Theme Editor: enable to make surfaceable via Liquid

To output in Liquid: `{{ product.metafields.custom.resin_color_notes }}`

---

## § PART 3 — Collections and Navigation

### Recommended collection structure for Glowmoon

| Collection | Handle | Contents |
|---|---|---|
| Doll Shop | `doll-shop` | All purchasable dolls |
| Full Sets | `full-set` | Dolls bundled with outfits/accessories |
| Blank Dolls | `blank` | Dolls without faceup for customizers |
| Accessories | `accessories` | Clothing, parts, extras |
| All Products | `all` (auto) | Shopify auto-collection |

Collections can be manual (curated) or automatic (rules-based).
For a small catalog, manual is simpler and safer.

### Navigation

Admin → Online Store → Navigation
- Main menu: top-level links (Shop, About, Care, Contact)
- Footer menu: policies, social, newsletter
- Keep main menu ≤ 5 items for mobile clarity

---

## § PART 4 — Theme Editor (No-Code Changes)

For changes Isabel can make without touching code:

1. Admin → Online Store → Themes → Customize
2. Use left panel to select/add/reorder sections
3. Click any section to edit its settings
4. Use the template dropdown (top center) to switch between page types

What can be changed in Theme Editor:
- Homepage layout and content blocks
- Colors, fonts, button styles (Theme Settings)
- Announcement bar text
- Featured collections
- Image banners and hero text

What requires code editing:
- Custom Liquid logic
- New section schemas
- CSS overrides beyond Theme Settings
- Snippet edits

---

## § PART 5 — Safe Code Editing Workflow

1. Admin → Online Store → Themes
2. Click "..." on active theme → Duplicate → rename "Dev copy — [date]"
3. Edit the duplicate: Actions → Edit code
4. Test thoroughly on duplicate
5. Publish duplicate when ready; old theme is preserved automatically

Shopify CLI (optional, for local dev):
```bash
npm install -g @shopify/cli @shopify/theme
shopify theme dev --store=boudi-doll.myshopify.com
```
Useful for complex Liquid work; not required for minor edits.

Theme Check (linter): Catches errors before deploying.
Run via Shopify CLI: `shopify theme check`

---

## § PART 6 — Metafields for Glowmoon-Specific Needs

Recommended metafield definitions to create:

| Namespace.key | Resource | Type | Purpose |
|---|---|---|---|
| `custom.resin_color_notes` | Product | Multi-line text | Color variance disclaimer per doll |
| `custom.faceup_instructions` | Product | Multi-line text | Specific faceup guidance |
| `custom.character_lore` | Product | Multi-line text | Character backstory (e.g., Rune's story) |
| `custom.measurements` | Product | Single-line text | Doll dimensions |
| `custom.compatible_accessories` | Product | Product reference list | Cross-link compatible items |

To display on product page: Add metafield reference in Theme Editor
(Dawn natively supports this in the product template) or via Liquid:
`{{ product.metafields.custom.character_lore }}`

---

## § PART 7 — Theme Migration: Debut → Dawn

When to migrate: Before doing any substantial Debut customization.
Once the Dawn migration is done, all future work builds on a maintained foundation.

What does NOT transfer automatically:
- Homepage section content (must be rebuilt in Dawn's editor)
- Any custom CSS/JS added to Debut
- Custom Liquid snippets
- Theme settings (colors, fonts)

What transfers automatically:
- All products, collections, pages, navigation menus
- Orders, customers, inventory
- Domain and Shopify settings

Migration steps (safe path):

1. Install Dawn from Theme Store (free) — do not publish yet
2. In Dawn's Theme Editor, rebuild homepage sections to match Debut layout
3. Copy any custom CSS from Debut assets to Dawn's `base.css`
4. Copy custom Liquid snippets as needed
5. Set up metafields in Dawn's product templates (native support)
6. Test all product pages, collections, cart, checkout
7. Test on mobile
8. When satisfied: publish Dawn; Debut remains as backup

Post-migration wins:
- Sections on every page (not just homepage)
- Native metafield display in Theme Editor
- App blocks (apps inject without theme code changes)
- 35% faster load time vs Debut
- Ongoing Shopify updates and support

---

## § PART 8 — Common Admin Tasks

### Add a new product
Admin → Products → Add product
- Title, description, media, pricing, inventory, variants, metafields
- Add to appropriate collection manually after saving

### Create a new page (About, FAQ, etc.)
Admin → Online Store → Pages → Add page
- Add to navigation via Admin → Online Store → Navigation

### Update announcement bar
Theme Editor → header section → Announcement bar text

### Set up international shipping exception
For case-by-case international orders (as Isabel's current policy):
- Admin → Settings → Shipping and delivery
- Default: US shipping rates
- International: "Contact us" or handle via draft orders

### Draft orders (for custom orders)
Admin → Orders → Create order
- Useful for custom commissions — build order manually, send invoice to customer
