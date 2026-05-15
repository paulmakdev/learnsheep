import { setUser } from "../features/user/userSlice";
import { store } from "../app/store";

export async function loadCurrentUser() {
  try {
    const apiUserInfoResponse = await fetch(`/api/me/info`);

    const apiUserInfo = await apiUserInfoResponse.json();

    const user = {
    email: apiUserInfo.email,
    role: apiUserInfo.role,
    displayName: apiUserInfo.display_name,
    createdAt: apiUserInfo.created_at,
    };

    store.dispatch(setUser(user));
  } catch (err) {
    console.error("Failed to load user", err);
  }
}
