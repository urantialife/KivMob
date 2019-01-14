from kivy.utils import platform
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView


if platform == 'android':
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        activity = autoclass('org.kivy.android.PythonActivity')
        AdListener = autoclass('com.google.android.gms.ads.AdListener')
        AdMobAdapter = autoclass('com.google.ads.mediation.admob.AdMobAdapter')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
        AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        AdSize = autoclass('com.google.android.gms.ads.AdSize')
        AdView = autoclass('com.google.android.gms.ads.AdView')
        Bundle = autoclass('android.os.Bundle')
        Gravity = autoclass('android.view.Gravity')
        InterstitialAd = autoclass('com.google.android.gms.ads.InterstitialAd')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams') 
        LinearLayout = autoclass('android.widget.LinearLayout')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        RewardItem = autoclass('com.google.android.gms.ads.reward.RewardItem')
        RewardedVideoAd = autoclass('com.google.android.gms.ads.reward.RewardedVideoAd')
        RewardedVideoAdListener = autoclass('com.google.android.gms.ads.reward.RewardedVideoAdListener')
        View = autoclass('android.view.View')

        class AdMobRewardedVideoAdListener(PythonJavaClass):

            __javainterfaces__ = ('com.google.android.gms.ads.reward.RewardedVideoAdListener', )
            __javacontext__ = 'app'

            @java_method('(Lcom.google.android.gms.ads.reward.RewardItem;)V')
            def onRewarded(self, reward):
                Logger.info('KivMob: onRewarded() called.')

            @java_method('()V')
            def onRewardedVideoAdLeftApplication(self):
                Logger.info('KivMob: onRewardedVideoAdLeftApplication() called.')

            @java_method('()V')
            def onRewardedVideoAdClosed(self):
                Logger.info('KivMob: onRewardedVideoAdClosed() called.')

            @java_method('(I)V')
            def onRewardedVideoAdFailedToLoad(self, errorCode):
                Logger.info('KivMob: onRewardedVideoAdFailedToLoad() called.')
                Logger.info('KivMob: ErrorCode ' + str(errorCode))

            @java_method('()V')
            def onRewardedVideoAdLoaded(self):
                Logger.info('KivMob: onRewardedVideoAdLoaded() called.')

            @java_method('()V')
            def onRewardedVideoAdOpened(self):
                Logger.info('KivMob: onRewardedVideoAdOpened() called.')

            @java_method('()V')
            def onRewardedVideoStarted(self):
                Logger.info('KivMob: onRewardedVideoStarted() called.')

            @java_method('()V')
            def onRewardedVideoCompleted(self):
                Logger.info('KivMob: onRewardedVideoCompleted() called.')
    except:
        Logger.error('KivMob: Cannot load AdMob classes. Check buildozer.spec configuration.')
else:
    class AdMobRewardedVideoAdListener():
        pass

    def run_on_ui_thread(x):
        pass


class MockBanner(RelativeLayout):
    pass


class TestIds():
    """ Enum of test ad ids provided by AdMob. This allows developers to test displaying ad
        without setting up an AdMob account.
    """

    APP = "ca-app-pub-3940256099942544~3347511713"
    BANNER =  "ca-app-pub-3940256099942544/6300978111"
    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"
    INTERSTITIAL_VIDEO = "ca-app-pub-3940256099942544/8691691433"
    REWARDED_VIDEO = "ca-app-pub-3940256099942544/5224354917"
    

class AdMobBridge():

    def __init__(self, appID):
        Logger.info('KivMob: __init__ called.')
        self.mock_banner = MockBanner()
        
    def add_test_device(self, testID):
        Logger.info('KivMob: add_test_device() called.')

    def is_interstitial_loaded(self):
        Logger.info('KivMob: is_interstitial_loaded() called.')
        return False
        
    def new_banner(self, unitID, top_pos=True):
        Logger.info('KivMob: new_banner() called.')
    
    def new_interstitial(self, unitID):
        Logger.info('KivMob: new_interstitial() called.')
    
    def request_banner(self, options):
        Logger.info('KivMob: request_banner() called.')

    def request_interstitial(self, options):
        Logger.info('KivMob: request_interstitial() called.')
        
    def show_banner(self):
        Logger.info('KivMob: show_banner() called.')

    def show_interstitial(self):
        Logger.info('KivMob: show_interstitial() called.')
    
    def destroy_banner(self):
        Logger.info('KivMob: destroy_banner() called.')

    def destroy_interstitial(self):
        Logger.info('KivMob: destroy_interstitial() called.')

    def hide_banner(self):
        Logger.info('KivMob: hide_banner() called.')
        from kivy.core.window import Window
        Window.remove_widget(self.mock_banner)

    def load_rewarded_ad(self, unitID):
        Logger.info('KivMob: load_rewarded_ad() called.')

    def show_rewarded_ad(self):
        Logger.info('KivMob: show_rewarded_ad() called.')

class AndroidBridge(AdMobBridge):

    @run_on_ui_thread
    def __init__(self, appID):
        self._loaded = False
        MobileAds.initialize(activity.mActivity, appID)
        self._adview = AdView(activity.mActivity)
        self._interstitial = InterstitialAd(activity.mActivity)
        self._listener = AdMobRewardedVideoAdListener()
        self._rewarded = MobileAds.getRewardedVideoAdInstance(activity.mActivity)
        self._rewarded.setRewardedVideoAdListener(self._listener)
        self._test_devices = []

    @run_on_ui_thread
    def add_test_device(self, testID):
        self._test_devices.append(testID)

    @run_on_ui_thread
    def new_banner(self, unitID, top_pos=True):
        self._adview = AdView(activity.mActivity)
        self._adview.setAdUnitId(unitID)
        self._adview.setAdSize(AdSize.SMART_BANNER)
        self._adview.setVisibility(View.GONE)
        adLayoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
        self._adview.setLayoutParams(adLayoutParams)
        layout = LinearLayout(activity.mActivity)
        if not top_pos:
            layout.setGravity(Gravity.BOTTOM)
        layout.addView(self._adview)
        layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        layout.setLayoutParams(layoutParams)
        activity.addContentView(layout, layoutParams)
        
    @run_on_ui_thread
    def request_banner(self, options={}):
        self._adview.loadAd(AdRequestBuilder().build())

    @run_on_ui_thread
    def show_banner(self):
        self._adview.setVisibility(View.VISIBLE)

    @run_on_ui_thread
    def hide_banner(self):
        self._adview.setVisibility(View.GONE)

    @run_on_ui_thread
    def new_interstitial(self, unitID):
        self._interstitial.setAdUnitId(unitID)

    @run_on_ui_thread
    def request_interstitial(self, options={}):
        builder = AdRequestBuilder()
        
        self._interstitial.loadAd(builder.build())

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        self._loaded = self._interstitial.isLoaded()

    def is_interstitial_loaded(self):
        # Values returned from run_on_ui_thread appear as
        # NoneType. Setting the result to private variable
        # self._loaded before returning solves this issue.
        self._is_interstitial_loaded()
        return self._loaded

    @run_on_ui_thread
    def show_interstitial(self):
        if self.is_interstitial_loaded():
            self._interstitial.show()

    @run_on_ui_thread
    def load_rewarded_ad(self, unitID):
        builder = self._get_builder(None)
        self._rewarded.loadAd(unitID, builder.build())

    @run_on_ui_thread
    def show_rewarded_ad(self):
        if self._rewarded.isLoaded():
            self._rewarded.show()

    @run_on_ui_thread
    def destroy_banner(self):
        self._adview.destroy()
    
    @run_on_ui_thread
    def destroy_interstitial(self):
        self._interstitial.destroy()

    @run_on_ui_thread
    def destroy_rewarded_video_ad(self):
        self._rewarded.destroy()

    @run_on_ui_thread
    def _get_builder(self, options):
        builder = AdRequestBuilder()
        if options is not None:
            if "children" in options:
                builder.tagForChildDirectedTreatment(options["children"])
            if "family" in options:
                extras = Bundle()
                extras.putBoolean("is_designed_for_families", options['family'])
                builder.addNetworkExtrasBundle(AdMobAdapter, extras)
        for test_device in self._test_devices:
            builder.addTestDevice(test_device)
        return builder


class iOSBridge(AdMobBridge):
    # TODO
    pass


class KivMob():
    ''' Allows access to AdMob functionality on Android devices.
    '''

    def __init__(self, appID):
        self._banner_top_pos = True
        if platform == 'android':
            Logger.info('KivMob: Android platform detected.')
            self.bridge = AndroidBridge(appID)
        elif platform == 'ios':
            Logger.warning('KivMob: iOS not yet supported.')
            self.bridge = iOSBridge(appID)
        else:
            Logger.warning('KivMob: Ads will not be shown.')
            self.bridge = AdMobBridge(appID)

    def add_test_device(self, device):
        ''' Add test device ID, which will tigger test ads to be displayed on that device

        :type device: string
        :param device: The test device ID of the physical android device you are testing on.
        '''
        self.bridge.add_test_device(device)
        
    def new_banner(self, unitID, top_pos=True):
        ''' Create a new mobile banner ad.

        :type unitID: string
        :param unitID: AdMob banner ID for mobile application.
        '''
        self._banner_top_pos = top_pos
        self.bridge.new_banner(unitID, top_pos)

    def new_interstitial(self, options={}):
        ''' Create a new mobile interstitial ad.
        '''
        self.bridge.new_interstitial(options)

    def is_interstitial_loaded(self):
        ''' Check if the interstitial ad has loaded.
        '''
        return self.bridge.is_interstitial_loaded()

    def request_banner(self, options={}):
        ''' Request a new banner ad from AdMob.
        '''
        self.bridge.request_banner(options)
        
    def request_interstitial(self, options={}):
        ''' Request a new interstitial ad from AdMob.
        '''
        self.bridge.request_interstitial(options)
        
    def show_banner(self):
        ''' Display banner ad.
        '''
        self.bridge.show_banner()

    def show_interstitial(self):
        ''' Display interstitial ad.
        '''
        self.bridge.show_interstitial()

    def destroy_banner(self):
        ''' Destroy banner ad.
        '''
        self.bridge.destroy_banner()

    def destroy_interstitial(self):
        ''' Destroy interstitial ad.
        '''
        self.bridge.destroy_interstitial()

    def hide_banner(self):
        '''  Hide current banner ad.
        '''
        self.bridge.hide_banner()

    def load_rewarded_ad(self, unitID):
        ''' Load ewarded video ad.
        '''
        self.bridge.load_rewarded_ad(unitID)

    def show_rewarded_ad(self):
        ''' Display rewarded video ad.
        '''
        self.bridge.show_rewarded_ad()


if __name__ == '__main__':
    print("\033[92m  _  ___       __  __       _\n" +\
          " | |/ (_)_   _|  \/  | ___ | |__\n" +\
          " | ' /| \ \ / / |\/| |/ _ \| '_ \\\n" +\
          " | . \| |\ V /| |  | | (_) | |_) |\n" +\
          " |_|\_\_| \_/ |_|  |_|\___/|_.__/\n\033[0m")
    print(" Michael Stott, 2019\n")
    
