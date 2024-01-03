handle = basic.get_handle()
print(f"底部{handle.bottom}, 顶部{handle.top}, 左边{handle.left}, 右边{handle.right}, 高{handle.bottom-handle.top}, 长{handle.right-handle.left}")
b, a = basic.get_screenshot(handle)

print(a.shape)
print(b.shape)

new_a = cv2.resize(a, (handle.right-handle.left, handle.bottom-handle.top))
print(new_a.shape)
cv2.imshow("1a", new_a)
cv2.waitKey(0)
cv2.destroyAllWindows()