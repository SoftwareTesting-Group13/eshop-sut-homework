# [BUG-GUI-04] Hai nút ở bước 2 Quên mật khẩu trông giống hệt nhau

**Severity:** Minor · **Priority:** Medium · **FR:** FR-03 — Quên mật khẩu · **Screen:** `/forgot-password`

## Mô tả

Cả hai đều là nút xanh lá full-width (`bg-green-600`), cùng kích thước và kiểu chữ; người dùng dễ bấm nhầm.

## Các bước tái hiện

1. Mở `/forgot-password`, nhập email đã đăng ký và bấm “Lấy mã OTP”.
2. So sánh nút “Đặt lại mật khẩu” và nút “← Quay lại”.

## Expected

Primary action nổi bật, dùng màu xanh dương theo FR-21; secondary/back rõ ràng là hành động phụ.

## Actual

Cả hai đều là nút xanh lá full-width (`bg-green-600`), cùng kích thước và kiểu chữ; người dùng dễ bấm nhầm.

## Checklist IDs

CHK-11

## Nguyên nhân

**[`frontend-web/src/pages/ForgotPassword.jsx:89`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L89)–[L95](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L95)**

```jsx
              
          <button type="submit" className="w-full bg-green-600 text-white py-2 rounded">
            Đặt lại mật khẩu
          </button>
          <button type="button" onClick={() => setStep(1)} className="w-full bg-green-600 text-white py-2 rounded">
            ← Quay lại
          </button>
```

Hai button dùng cùng class `w-full bg-green-600 text-white`.

## Đề xuất sửa

Render nút quay lại dạng text/outline và giữ primary action là nút filled màu xanh dương.

## Screenshots

![BUG-GUI-04](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-11-forgot-buttons.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
