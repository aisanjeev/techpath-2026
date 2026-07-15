# Dynamic FAQs for Services - Implementation Summary

## ✅ Backend (COMPLETE)

1. **Model** (`app/models/service.py`):
   - Added `faqs` column (Text, nullable, stores JSON)

2. **Schemas** (`app/schemas/service.py`):
   - Added `ServiceFAQItem` class (question, answer)
   - Added `faqs: Optional[List[ServiceFAQItem]]` to ServiceCreate, ServiceUpdate, ServiceResponse

3. **CRUD** (`app/crud/service.py`):
   - Updated `create()` to serialize faqs to JSON
   - Updated `update()` to serialize faqs to JSON
   - Updated `model_validate()` to deserialize faqs from JSON

4. **Migration** (`versions/20260131_services_add_faqs.py`):
   - Created migration to add `faqs` column to services table
   - Revision ID: `j0k1l2m3n4o5`
   - Revises: `i9j0k1l2m3n4` (SEO fields migration)

## ✅ Admin Panel (COMPLETE)

1. **Types** (`src/types/api.ts`):
   - Added `ServiceFAQItem` interface
   - Added `faqs?: ServiceFAQItem[]` to Service and ServiceCreate

2. **Validation** (`src/lib/validations.ts`):
   - Added `serviceFAQItemSchema` with question/answer validation
   - Added `faqs` field to serviceSchema

## 🔄 TODO: Admin Form UI

Add FAQs section to `ServiceForm.tsx` (after CTA section, before sidebar):

```tsx
<Card>
  <CardHeader>
    <CardTitle>FAQs</CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    {faqs.map((_, i) => (
      <div key={i} className="space-y-2 rounded-lg border border-slate-700 p-4">
        <FormField label={`Question ${i + 1}`} error={errors.faqs?.[i]?.question?.message}>
          <Input
            value={faqs[i]?.question || ''}
            onChange={(e) => {
              const next = [...faqs];
              next[i] = { ...next[i], question: e.target.value };
              setValue('faqs', next);
            }}
            placeholder="e.g., How long does implementation take?"
          />
        </FormField>
        <FormField label="Answer" error={errors.faqs?.[i]?.answer?.message}>
          <Textarea
            value={faqs[i]?.answer || ''}
            onChange={(e) => {
              const next = [...faqs];
              next[i] = { ...next[i], answer: e.target.value };
              setValue('faqs', next);
            }}
            placeholder="Detailed answer..."
            rows={3}
          />
        </FormField>
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => setValue('faqs', faqs.filter((_, j) => j !== i))}
        >
          Remove FAQ
        </Button>
      </div>
    ))}
    <Button
      type="button"
      variant="outline"
      onClick={() => setValue('faqs', [...faqs, { question: '', answer: '' }])}
    >
      Add FAQ
    </Button>
  </CardContent>
</Card>
```

And in defaultValues:
```tsx
faqs: initialData?.faqs || [],
```

And in watch:
```tsx
const faqs = watch('faqs') || [];
```

## 🔄 TODO: Frontend

1. **Service Interface** (`src/services/serviceService.ts`):
   - Add `faqs?: { question: string; answer: string }[]` to ServiceItem interface

2. **Service Detail Page** (`src/pages/services/[slug].astro`):
   - Replace hardcoded `serviceFaqs` array with:
   ```tsx
   const serviceFaqs = service.faqs || defaultFallbackFaqs;
   ```

## 📝 Next Steps

1. Run migration: `poetry run alembic upgrade head`
2. Add FAQs UI to ServiceForm.tsx (see above)
3. Update frontend serviceService.ts interface
4. Update [slug].astro to use dynamic FAQs
5. Run seeding script with FAQs included
6. Build and test!
