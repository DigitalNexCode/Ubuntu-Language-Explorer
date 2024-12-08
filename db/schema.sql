-- Enable Row Level Security
ALTER TABLE app_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE translations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

-- Create app_users table
CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    last_sign_in TIMESTAMP WITH TIME ZONE,
    preferences JSONB DEFAULT '{}'::jsonb,
    learning_points INTEGER DEFAULT 0,
    daily_streak INTEGER DEFAULT 0,
    total_translations INTEGER DEFAULT 0,
    profile_picture_url TEXT,
    preferred_language VARCHAR(50) DEFAULT 'Zulu'
);

-- Create translations table
CREATE TABLE translations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_users(id),
    source_lang TEXT NOT NULL,
    target_lang TEXT NOT NULL,
    source_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    cultural_context TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create user_progress table
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_users(id),
    module_id TEXT NOT NULL,
    progress JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    UNIQUE(user_id, module_id)
);

-- Create favorites table
CREATE TABLE favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_users(id),
    content_type TEXT NOT NULL,
    content_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    UNIQUE(user_id, content_type, content_id)
);

-- Create language_training table
CREATE TABLE IF NOT EXISTS language_training (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES app_users(id),
    language TEXT NOT NULL,
    phrase TEXT NOT NULL,
    translation TEXT NOT NULL,
    context TEXT,
    validation_status TEXT DEFAULT 'pending',
    validation_count INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create training_validations table
CREATE TABLE IF NOT EXISTS training_validations (
    id SERIAL PRIMARY KEY,
    training_id INTEGER NOT NULL REFERENCES language_training(id),
    user_id UUID NOT NULL REFERENCES app_users(id),
    status TEXT NOT NULL,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create RLS Policies

-- app_users policies
CREATE POLICY "Users can view own profile"
    ON app_users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON app_users FOR UPDATE
    USING (auth.uid() = id);

-- translations policies
CREATE POLICY "Users can view own translations"
    ON translations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create translations"
    ON translations FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- user_progress policies
CREATE POLICY "Users can view own progress"
    ON user_progress FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
    ON user_progress FOR ALL
    USING (auth.uid() = user_id);

-- favorites policies
CREATE POLICY "Users can manage own favorites"
    ON favorites FOR ALL
    USING (auth.uid() = user_id);

-- Create indexes for better performance
CREATE INDEX idx_translations_user_id ON translations(user_id);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_translations_langs ON translations(source_lang, target_lang);

-- Create function to check if username exists
CREATE OR REPLACE FUNCTION public.check_username_exists(username_to_check TEXT)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN jsonb_build_object(
        'exists',
        EXISTS (
            SELECT 1 FROM app_users
            WHERE preferences->>'username' = username_to_check
        )
    );
END;
$$;

-- Create function to check if email exists
CREATE OR REPLACE FUNCTION public.check_email_exists(email_to_check TEXT)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN jsonb_build_object(
        'exists',
        EXISTS (
            SELECT 1 FROM app_users
            WHERE email = email_to_check
        )
    );
END;
$$;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, service_role;
