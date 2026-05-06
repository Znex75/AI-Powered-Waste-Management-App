package com.ecocycle.wastemanagement;

import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import androidx.annotation.NonNull;
import com.facebook.AccessToken;
import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.login.LoginManager;
import com.facebook.login.LoginResult;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthCredential;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FacebookAuthProvider;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.GoogleAuthProvider;
import java.util.Arrays;

/**
 * Helper class for Google and Facebook authentication using Firebase Auth
 */
public class AuthHelper {
    private static final String TAG = "AuthHelper";
    private static final int RC_GOOGLE_SIGN_IN = 9001;

    private final Activity activity;
    private final FirebaseAuth firebaseAuth;
    private final GoogleSignInClient googleSignInClient;
    private final CallbackManager facebookCallbackManager;
    private final AuthCallback authCallback;

    public interface AuthCallback {
        void onAuthSuccess(FirebaseUser user);
        void onAuthFailure(String error);
    }

    public AuthHelper(Activity activity, AuthCallback callback) {
        this.activity = activity;
        this.authCallback = callback;
        this.firebaseAuth = FirebaseAuth.getInstance();
        this.facebookCallbackManager = CallbackManager.Factory.create();

        // Configure Google Sign In
        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestIdToken(activity.getString(R.string.default_web_client_id))
                .requestEmail()
                .build();
        this.googleSignInClient = GoogleSignIn.getClient(activity, gso);

        setupFacebookCallback();
    }

    private void setupFacebookCallback() {
        LoginManager.getInstance().registerCallback(facebookCallbackManager,
            new FacebookCallback<LoginResult>() {
                @Override
                public void onSuccess(LoginResult loginResult) {
                    Log.d(TAG, "Facebook login success");
                    handleFacebookAccessToken(loginResult.getAccessToken());
                }

                @Override
                public void onCancel() {
                    Log.d(TAG, "Facebook login cancelled");
                    authCallback.onAuthFailure("Facebook login cancelled");
                }

                @Override
                public void onError(FacebookException exception) {
                    Log.e(TAG, "Facebook login error", exception);
                    authCallback.onAuthFailure("Facebook login failed: " + exception.getMessage());
                }
            });
    }

    /**
     * Start Google Sign In flow
     */
    public void signInWithGoogle() {
        Intent signInIntent = googleSignInClient.getSignInIntent();
        activity.startActivityForResult(signInIntent, RC_GOOGLE_SIGN_IN);
    }

    /**
     * Start Facebook Sign In flow
     */
    public void signInWithFacebook() {
        LoginManager.getInstance().logInWithReadPermissions(activity,
            Arrays.asList("email", "public_profile"));
    }

    /**
     * Handle activity result for authentication
     */
    public void handleActivityResult(int requestCode, int resultCode, Intent data) {
        // Handle Facebook callback
        facebookCallbackManager.onActivityResult(requestCode, resultCode, data);

        // Handle Google Sign In
        if (requestCode == RC_GOOGLE_SIGN_IN) {
            Task<GoogleSignInAccount> task = GoogleSignIn.getSignedInAccountFromIntent(data);
            try {
                GoogleSignInAccount account = task.getResult(ApiException.class);
                firebaseAuthWithGoogle(account.getIdToken());
            } catch (ApiException e) {
                Log.e(TAG, "Google sign in failed", e);
                authCallback.onAuthFailure("Google sign in failed: " + e.getMessage());
            }
        }
    }

    private void firebaseAuthWithGoogle(String idToken) {
        AuthCredential credential = GoogleAuthProvider.getCredential(idToken, null);
        firebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(activity, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            Log.d(TAG, "Google sign in with Firebase success");
                            FirebaseUser user = firebaseAuth.getCurrentUser();
                            authCallback.onAuthSuccess(user);
                        } else {
                            Log.e(TAG, "Google sign in with Firebase failed", task.getException());
                            authCallback.onAuthFailure("Firebase authentication failed: " +
                                task.getException().getMessage());
                        }
                    }
                });
    }

    private void handleFacebookAccessToken(AccessToken token) {
        Log.d(TAG, "handleFacebookAccessToken:" + token);

        AuthCredential credential = FacebookAuthProvider.getCredential(token.getToken());
        firebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(activity, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            Log.d(TAG, "Facebook sign in with Firebase success");
                            FirebaseUser user = firebaseAuth.getCurrentUser();
                            authCallback.onAuthSuccess(user);
                        } else {
                            Log.e(TAG, "Facebook sign in with Firebase failed", task.getException());
                            authCallback.onAuthFailure("Firebase authentication failed: " +
                                task.getException().getMessage());
                        }
                    }
                });
    }

    /**
     * Sign out from all providers
     */
    public void signOut() {
        firebaseAuth.signOut();
        googleSignInClient.signOut();
        LoginManager.getInstance().logOut();
    }

    /**
     * Get current Firebase user
     */
    public FirebaseUser getCurrentUser() {
        return firebaseAuth.getCurrentUser();
    }
}