using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using GameNetcodeStuff;
using UnityEngine.Networking;
using System.Collections;
using UnityEngine;

namespace PostChatPlugin
{
    [BepInPlugin("walksanator.PostChat", "Post Chat", "1.0.0")]
    public class PostChatPlugin : BaseUnityPlugin
    {
        internal new static ManualLogSource Logger { get; private set; }
        internal static PostChatPlugin Instance { get; private set; }
        private void Awake()
        {
            Logger = base.Logger;
            Instance = this;
            Logger.LogInfo($"C# Instance {this} or {Instance}");
            // Plugin startup logic
            Logger.LogInfo("Post Chat: performing patches");
            Harmony.CreateAndPatchAll(typeof(PostChatPlugin));
            Logger.LogInfo($"Plugin walksanator.PostChat is loaded!");
            Logger.LogInfo($"Just Checking {Instance}");
        }

        [HarmonyPostfix]
        [HarmonyPatch(typeof(HUDManager), "AddTextToChatOnServer")]
        static void PostChatHttp(ref string chatMessage, ref int playerId)
        {
            Logger.LogInfo($"You SAID: {chatMessage}");
            Logger.LogInfo($"C# Instance {Instance}");
            if (PostChatPlugin.Instance != null)
            {
                PostChatPlugin.Instance.StartCoroutine(SendPostRequest(chatMessage)); //HERE
                Logger.LogInfo($"Post SEND: {chatMessage}");
            }
            else
            {
                Logger.LogError("Instance is null!");
            }
        }


        static IEnumerator SendPostRequest(string message)
        {
            // URL to send the POST request to
            string url = "http://127.0.0.1:5000";
            Logger.LogInfo("Building headers");
            // Create a UnityWebRequest and set its method to POST
            UnityWebRequest request = UnityWebRequest.Post(url, message, "text/plain");

            Logger.LogInfo("Build request");
            // Send the request and wait for a response
            yield return request.SendWebRequest();
            Logger.LogInfo("Post Request");
            // Check for errors
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
            }
            else
            {
                // Request was successful, do something with the response
                Debug.Log("Response: " + request.downloadHandler.text);
            }
        }

    }
}